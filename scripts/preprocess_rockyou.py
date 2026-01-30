import sys
from pathlib import Path
import hashlib
import pickle
from collections import Counter
from pathlib import Path
from tqdm import tqdm
from core.features import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

RAW_PATH = Path("data/raw/rockyou.txt")
PKL_OUT_PATH = Path("data/processed/rockyou_hashes.pkl")
FEATURES_OUT_PATH = Path("data/processed/rockyou_features.pkl")

features = {}

def hash_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def main():
    counts = Counter()
    # buffering is used to read in larger chunks
    with open(RAW_PATH, "r", errors="ignore", buffering=1024*1024) as f:
        for line in tqdm(f, desc="Processing passwords"):
            pw = line.strip()

            if not pw:
                continue

            h = hash_sha256(pw)
            counts[h] += 1
            if h not in features:
                features[h] = get_features(pw)

    PKL_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PKL_OUT_PATH, "wb") as f:
        pickle.dump(counts, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open(FEATURES_OUT_PATH, "wb") as f:
        pickle.dump(features, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Processed {sum(counts.values())} passwords")
    print(f"Unique hashes: {len(counts)}")
    print(f"Saved hashes to {PKL_OUT_PATH}")
    print(f"Saved features to {FEATURES_OUT_PATH}")

if __name__ == "__main__":
    main()