import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.features import get_features
from core.entropy import shannon_entropy, policy_entropy
import pickle

with open("ml/password_model.pkl", "rb") as f:
    model = pickle.load(f)

tests = ["password", "123456", "Fluffy2019!", "correct-horse-battery", "xK9#mPqL2$vR"]

for pw in tests:
    features = get_features(pw)
    length = features["length"]
    vector = [length, shannon_entropy(pw), policy_entropy(pw),
              features["digits_count"]/length, features["symbol_count"]/length,
              features["upper_count"]/length, features["lower_count"]/length,
              features["repeated_chars"], features["sequential_chars"],
              int(features["dictionary_word"]), int(features["date_pattern"])]
    
    pred = model.predict([vector])[0]
    labels = {0: "weak", 1: "medium", 2: "strong"}
    print(f"{pw:30s} → {labels[pred]}")