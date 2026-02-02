import pickle
from pathlib import Path

PROCESSED_PATH = Path("data/processed/rockyou_features.pkl")

_features = None

def load_rockyou_features():
    global _features
    if _features is None:
        with open(PROCESSED_PATH, "rb") as f:
            _features = pickle.load(f)

    return _features

def get_features_by_hash(pw_hash):
    features = load_rockyou_features()
    return features.get(pw_hash)