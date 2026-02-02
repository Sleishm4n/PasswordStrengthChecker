import pickle
from pathlib import Path

PROCESSED_PATH = Path("data/processed/rockyou_hashes.pkl")

_hashes = None

def load_rockyou_hashes() -> set:
    global _hashes
    if _hashes is None:
        with open(PROCESSED_PATH, "rb") as f:
            _hashes = pickle.load(f)

    return _hashes

def rockyou_contains(pw_hash):
    hashes = load_rockyou_hashes()
    return pw_hash in hashes
