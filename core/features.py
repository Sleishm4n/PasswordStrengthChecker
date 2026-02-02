import re
import urllib.request
import ahocorasick
from datetime import datetime
from pathlib import Path

DICT_WORDS_PATH = Path("data/raw/words.txt")
DATE_FORMATS =  ("%d%m%y", "%d%m%Y", "%Y%m%d")

AUTOMATON = None

def count_consecutive_repeated_chars(password):
    return sum(1 for a, b in zip(password, password[1:]) if a == b)

def download_word_list():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

    if not DICT_WORDS_PATH.exists():
        print("\nDownloading word list...")
        urllib.request.urlretrieve(url, DICT_WORDS_PATH)
        print(f"Downloaded to {DICT_WORDS_PATH}")
    
def load_automaton():
    global AUTOMATON
    if AUTOMATON is None:
        AUTOMATON = ahocorasick.Automaton()

        download_word_list()

        word_count = 0
        with open(DICT_WORDS_PATH, encoding="utf8", errors="ignore") as f:
            for word in f:
                word = word.strip().lower()
                if len(word) > 3:
                    AUTOMATON.add_word(word, word)
                    word_count += 1

        AUTOMATON.make_automaton()
    
    return AUTOMATON

def contains_dictionary_word(password, min_length=3):
    automaton = load_automaton()
    password_lower = password.lower()

    for end_i, found_word in automaton.iter(password_lower):
        if len(found_word) >= min_length:
            return True
    return False

def contains_date(password):
    candidates = re.findall(r"\d{6,8}", password)

    for chunk in candidates:
        for format in DATE_FORMATS:
            try:
                datetime.strptime(chunk, format)
                return True
            except ValueError:
                pass

    return False

def get_features(password):
    n = len(password)
    seen = set()

    # single pass through password to improve efficieny
    digits = upper = symbols = lower = 0

    for c in password:
        seen.add(c)
        if c.isdigit():
            digits += 1
        elif c.isupper():
            upper += 1
        elif not c.isalnum():
            symbols += 1
        elif c.islower():
            lower += 1

    n_uniq = len(seen)
    has_letters = lower + upper > 3

    return {
        "length": n,
        "unique_char": n_uniq,
        "digits_count": digits,
        "symbol_count": symbols,
        "upper_count": upper,
        "lower_count": lower,
        "repeated_chars": n - n_uniq,
        "sequential_chars": count_consecutive_repeated_chars(password),
        "dictionary_word": has_letters and contains_dictionary_word(password),
        "date_pattern": contains_date(password),
    }