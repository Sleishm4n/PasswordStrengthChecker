import hashlib
import pickle
# import enchant
from collections import Counter
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

RAW_PATH = Path("../data/raw/rockyou.txt")
PKL_OUT_PATH = Path("../data/processed/rockyou_hashes.pkl")
FEATURES_OUT_PATH = Path("../data/processed/rockyou_features.pkl")
# ENG_DICT = enchant.Dict("en_GB")

features = {}

def hash_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def count_consecutive_repeated_chars(password):
    count = 0
    for i in range(len(password)-1):
        if password[i] == password[i+1]:
            count += 1
    return count

# def contains_dictionary_word(password, min_length = 3):
#     password = password.lower()
#     n = len(password)

#     for i in range(n):
#         for j in range(i + min_length, n + 1):
#             if ENG_DICT.check(password[i:j]):
#                 return True
#     return False

def contains_date(password):
    for fmt in ("%d%m%y", "%d%m%Y", "%Y%m%d"):
        try:
            datetime.strptime(password, fmt)
            return True
        except ValueError:
            continue
    return False

def get_features(password):
    uniq = set(password)
    n = len(password)
    n_uniq = len(uniq)

    return {
        "length": n,
        "unique_char": n_uniq,
        "digits_count": sum(c.isdigit() for c in password),
        "symbol_count": sum(not c.isalnum() for c in password),
        "upper_count": sum(c.isupper() for c in password),
        "lowercase_count": sum(c.islower() for c in password),
        "repeated_chars": n - n_uniq,
        "sequential_chars": count_consecutive_repeated_chars(password),
        # "dictionary_word": contains_dictionary_word(password),
        "date_pattern": contains_date(password),
    }

def main():
    counts = Counter()

    with open(RAW_PATH, "r", errors="ignore") as f:
        for line in tqdm(f, desc="Processing passwords"):
            pw = line.strip()

            if not pw:
                continue

            h = hash_sha256(pw)
            counts[h] += 1
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