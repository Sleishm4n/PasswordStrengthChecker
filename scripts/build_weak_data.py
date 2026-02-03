import pickle
import sys
from pathlib import Path
from tqdm.auto import tqdm
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.entropy import shannon_entropy, policy_entropy

ROCKYOU_FEATURES = Path("data/processed/rockyou_features.pkl")
OUT_PATH = Path("data/processed/weak_dataset.pkl")

def main():
    with open(ROCKYOU_FEATURES, "rb") as f:
        rockyou = pickle.load(f)

    x, y = [], []

    for feature in tqdm(rockyou.values()):
        length = feature["length"]

        shan = length * 2
        pol = length * 2

        vector = [
            feature["length"],
            shan,
            pol,
            feature["digits_count"] / length if length else 0,
            feature["symbol_count"] / length if length else 0,
            feature["upper_count"] / length if length else 0,
            feature["lower_count"] / length if length else 0,
            feature["repeated_chars"],
            feature["sequential_chars"],
            int(feature["dictionary_word"]),
            int(feature["date_pattern"]),
        ]

        x.append(vector)
        y.append(0)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "wb") as f:
        pickle.dump((x, y), f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Saved {len(x)} weak samples")

if __name__ == "__main__":
    main()
