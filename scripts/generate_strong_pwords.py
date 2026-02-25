import random
import string
import pickle
import sys
from pathlib import Path
from tqdm.auto import tqdm
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.features import get_features
from core.entropy import shannon_entropy, policy_entropy

OUT_PATH = Path("data/processed/synth_strong.pkl")

SYMBOLS = "!$%^&*()_+-=[]{}:;@'~#<,>.?/|\\"

def generate_strong(min_length=12, max_length=20):
    length = random.randint(min_length, max_length)

    chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(SYMBOLS)
    ]

    pool = string.ascii_letters + string.digits + SYMBOLS

    chars += random.choices(pool, k=length -4)
    random.shuffle(chars)

    return "".join(chars)

def main(n=50_000):
    x = []
    y = []

    for _ in tqdm(range(n)):
        pw = generate_strong()

        features = get_features(pw)
        shan = shannon_entropy(pw)
        pol = policy_entropy(pw)

        vector = [
            features["length"],
            shan,
            pol,
            features["digits_count"] / features["length"],
            features["symbol_count"] / features["length"],
            features["upper_count"] / features["length"],
            features["lower_count"] / features["length"],
            features["repeated_chars"],
            features["sequential_chars"],
            int(features["dictionary_word"]),
            int(features["date_pattern"]),        
        ]

        x.append(vector)
        y.append(2)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_PATH, "wb") as f:
        pickle.dump((x, y), f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Saved {len(x)} strong sythentic passwords")
 
if __name__ == "__main__":
    main()