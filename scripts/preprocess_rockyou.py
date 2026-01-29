import hashlib
import json
import time
import pickle
from collections import Counter
from pathlib import Path
from tqdm import tqdm

RAW_PATH = Path("../data/raw/rockyou.txt")
JSON_OUT_PATH = Path("../data/processed/rockyou_hashes.json")
PKL_OUT_PATH = Path("../data/processed/rockyou_hashes.pkl")


def hash_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def main():
    counts = Counter()

    with open(RAW_PATH, "r", errors="ignore") as f:
        for line in tqdm(f, desc="Hashing passwords"):
            pw = line.strip().lower()

            if not pw:
                continue

            h = hash_sha256(pw)
            counts[h] += 1

    JSON_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(JSON_OUT_PATH, "w") as f:
        json.dump(dict(counts), f)

    with open(PKL_OUT_PATH, "wb") as f:
        pickle.dump(counts, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Processed {sum(counts.values())} passwords")
    print(f"Unique hashes: {len(counts)}")
    print(f"Saved JSON to {JSON_OUT_PATH}")
    print(f"Saved JSON to {PKL_OUT_PATH}")

if __name__ == "__main__":
    main()