import pickle
from pathlib import Path

WEAK = Path("data/processed/weak_dataset.pkl")
STRONG = Path("data/processed/synth_strong.pkl")

OUT = Path("data/processed/ml_data.pkl")

def main():
    with open(WEAK, "rb") as f:
        Xw, yw = pickle.load(f)

    with open(STRONG, "rb") as f:
        Xs, ys = pickle.load(f)

    X = Xw + Xs
    y = yw + ys

    with open(OUT, "wb") as f:
        pickle.dump((X, y), f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Total samples: {len(X)}") 
    print(f"Weak: {len(Xw)}")
    print(f"Strong: {len(Xs)}")

if __name__ == "__main__":
    main()