import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.features import get_features
from core.entropy import shannon_entropy, policy_entropy

MODEL_PATH = Path("ml/password_model.pkl")

_model = None


def load_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def build_vector(password: str) -> list:
    features = get_features(password)
    length = features["length"] or 1
    return [
        length,
        shannon_entropy(password),
        policy_entropy(password),
        features["digits_count"] / length,
        features["symbol_count"] / length,
        features["upper_count"] / length,
        features["lower_count"] / length,
        features["repeated_chars"],
        features["sequential_chars"],
        int(features["dictionary_word"]),
        int(features["date_pattern"]),
    ]


def ml_score(password: str) -> dict:
    model = load_model()
    vector = build_vector(password)
    proba = model.predict_proba([vector])[0]

    score = (proba[0] * 0) + (proba[1] * 50) + (proba[2] * 100)

    return {
        "ml_score": round(score, 1),
        "p_weak": round(proba[0], 3),
        "p_medium": round(proba[1], 3),
        "p_strong": round(proba[2], 3),
    }
