import pickle
import random
from pathlib import Path

WEAK = Path("data/processed/weak_dataset.pkl")
MEDIUM = Path("data/processed/synth_medium.pkl")
STRONG = Path("data/processed/synth_strong.pkl")

OUT = Path("data/processed/ml_data.pkl")

def main():
    with open(WEAK, "rb") as f:
        Xw, yw = pickle.load(f)

    with open(MEDIUM, "rb") as f:
        Xm, ym = pickle.load(f)

    with open(STRONG, "rb") as f:
        Xs, ys = pickle.load(f)

    sample_size = 150_000
    indices = random.sample(range(len(Xw)), sample_size)
    Xw = [Xw[i] for i in indices]
    yw = [yw[i] for i in indices]

    X = Xw + Xm + Xs
    y = yw + ym + ys

    with open(OUT, "wb") as f:
        pickle.dump((X, y), f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Total samples: {len(X)}") 
    print(f"Weak: {len(Xw)}")
    print(f"Medium: {len(Xm)}")
    print(f"Strong: {len(Xs)}")

if __name__ == "__main__":
    main()