import random
import string
import pickle
import sys
from pathlib import Path
from tqdm.auto import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.entropy import policy_entropy, shannon_entropy
from core.features import get_features


SYMBOLS = "!$%^&*()_+-=[]{}:;@'~#<,>.?/|\\"
COMMON_SUBSTITUTIONS = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "+"}

DICT_WORDS_PATH = Path("data/raw/words.txt")
OUT_PATH = Path("data/processed/synth_medium.pkl")


def load_words(min_len=4, max_len=8):
    with open(DICT_WORDS_PATH) as f:
        return [w.strip().lower() for w in f if min_len <= len(w.strip()) <= max_len]


def gen_word_number(words):
    word = random.choice(words)
    number = random.randint(1, 9999)
    return f"{word}{number}"


def gen_word_number_symbol(words):
    word = random.choice(words)
    number = random.randint(1, 9999)
    sybmbol = random.choice(SYMBOLS)
    return f"{word}{number}{sybmbol}"


def gen_leet_speak(words):
    word = random.choice(words)
    result = ""
    for ch in word:
        if ch in COMMON_SUBSTITUTIONS and random.random() > 0.4:
            result += COMMON_SUBSTITUTIONS[ch]
        else:
            result += ch
    return result + str(random.randint(0, 99))


def gen_two_words(words):
    w1 = random.choice(words)
    w2 = random.choice(words)
    sep = random.choice(["", "_", "-", "."])
    capitalize = random.random() > 0.5
    if capitalize:
        return w1.capitalize() + sep + w2.capitalize()
    return w1 + sep + w2


def gen_keyboard_walk():
    walks = [
        "qwerty",
        "qwertyuiop",
        "asdfgh",
        "zxcvbn",
        "1qaz2wsx",
        "qazwsx",
        "1q2w3e",
        "qweasd",
    ]
    base = random.choice(walks)
    suffix = str(random.randint(1, 999))
    symbol = random.choice(SYMBOLS) if random.random() > 0.5 else ""
    return base.capitalize() + suffix + symbol


def gen_name_date(words):
    name = random.choice([w for w in words if 3 <= len(w) <= 6]).capitalize()
    year = random.randint(1970, 2005)
    symbol = random.choice(SYMBOLS) if random.random() > 0.6 else ""
    return f"{name}{year}{symbol}"


def gen_repeated_pattern():
    base = random.choice(string.ascii_lowercase) * random.randint(2, 4)
    extra = random.choice(["123", "abc", "111", "xyz"])
    return base + extra + random.choice(SYMBOLS)


GENERATORS = [
    gen_word_number,
    gen_word_number_symbol,
    gen_leet_speak,
    gen_two_words,
    gen_keyboard_walk,
    gen_name_date,
    gen_repeated_pattern,
]

NEEDS_WORDS = {
    gen_word_number,
    gen_word_number_symbol,
    gen_leet_speak,
    gen_two_words,
    gen_name_date,
}


def generate_med(words):
    gen = random.choice(GENERATORS)
    if gen in NEEDS_WORDS:
        return gen(words)
    return gen()


def build_vector(pw: str) -> list:
    features = get_features(pw)
    length = features["length"] or 1
    shan = shannon_entropy(pw)
    pol = policy_entropy(pw)
    return [
        length,
        shan,
        pol,
        features["digits_count"] / length,
        features["symbol_count"] / length,
        features["upper_count"] / length,
        features["lower_count"] / length,
        features["repeated_chars"],
        features["sequential_chars"],
        int(features["dictionary_word"]),
        int(features["date_pattern"]),
    ]


def main(n=50_000):
    words = load_words()

    x, y = [], []

    for i in tqdm(range(n), desc="Generating medium passwords"):
        pword = generate_med(words)
        x.append(build_vector(pword))
        y.append(1)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        pickle.dump((x, y), f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Saved {len(x)} medium synthetic passwords to {OUT_PATH}")


if __name__ == "__main__":
    main()
