import pickle
from pathlib import Path

PROCESSED_PATH = Path("data/processed/rockyou_features.pkl")

def load_rockyou_features() -> set:
    # Load the RockYou password features as a set
    with open(PROCESSED_PATH, "rb") as f:
        return pickle.load(f)

rockyou_features = load_rockyou_features()