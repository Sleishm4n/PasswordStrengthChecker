import pickle
from pathlib import Path

PROCESSED_PATH = Path("data/processed/rockyou_hashes.pkl")

def load_rockyou_hashes() -> set:
    # Load the RockYou password hashes as a set
    with open(PROCESSED_PATH, "rb") as f:
        return pickle.load(f)

rockyou_hashes = load_rockyou_hashes()