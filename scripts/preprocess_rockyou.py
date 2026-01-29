import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from tqdm import tqdm

RAW_PATH = Path("../data/raw/rockyou.txt")
OUT_PATH = Path("../data/processed/rockyou_hashes.json")

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

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "w") as f:
        json.dump(dict(counts), f)

    print(f"Processed {sum(counts.values())} passwords")
    print(f"Unique hashes: {len(counts)}")
    print(f"Saved to {OUT_PATH}")

if __name__ == "__main__":
    main()