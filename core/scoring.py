import sys
from pathlib import Path
from blacklist import blacklist
from features import get_features
from entropy import shannon_entropy, policy_entropy

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.predictor import ml_score as get_ml_score

def get_usr_pw():
    return input("Enter a password: ").strip()

def normalise(x, low=0, high=100):
    return max(low, min(x, high))
     
def score_password(features, shan_entropy, leaked, password):
    score = 100
    reasons = []

    length = features['length']

    if leaked:
        score = min(score, 20)
        reasons.append("Appears in data leak")

    if length < 8:
        score -= 25
        reasons.append("Password is very short")
    elif length < 12:
        score -= 10
        reasons.append("Password could be longer")

    if shan_entropy < 2.5:
        score -= 20
        reasons.append("Entropy is low for length")
    elif shan_entropy < 3.2:
        score -= 10

    variety = 0

    if features['digits_count'] > 0:
        variety += 1
    if features['upper_count'] > 0:
        variety += 1
    if features['lower_count'] > 0:
        variety += 1
    if features['symbol_count'] > 0:
        variety += 1

    if variety <= 1:
        score -= 15
    elif variety == 2:
        score -= 5

    if features["dictionary_word"]:
        score -= 20
        reasons.append("Contains dictionary word")

    if features["date_pattern"]:
        score -= 15
        reasons.append("Contains date pattern")

    if features["sequential_chars"] >= 2:
        score -= 10
        reasons.append("Has repeated character runs")

    if features["repeated_chars"] > features["length"] * 0.6:
        score -= 10
        reasons.append("Too many repeated characters overall")

    if score >= 80:
        ML_WEIGHT = 0.1
        RULE_WEIGHT = 0.9
    elif score >= 60:
        ML_WEIGHT = 0.3
        RULE_WEIGHT = 0.7
    else:
        ML_WEIGHT = 0.5
        RULE_WEIGHT = 0.5

    ml = get_ml_score(password)
    ml_adjusted = max(ml["ml_score"], score * 0.6)
    final_score = (RULE_WEIGHT * score) + (ML_WEIGHT * ml_adjusted)
    final_score = normalise(final_score)

    if final_score < 20:
        label = "Very Weak"
    elif final_score < 40:
        label = "Weak"
    elif final_score < 60:
        label = "Medium"
    elif final_score < 80:
        label = "Strong"
    else:
        label = "Very Strong"

    return {
        "score": round(final_score),
        "label": label,
        "entropy": round(shan_entropy, 2),  # keep using real shannon here
        "reasons": reasons,
        "ml": ml,  # expose probabilities for UI later
    }

def main():
    pw = get_usr_pw()

    leaked = blacklist(pw)
    
    features = get_features(pw)
    shan_entropy = shannon_entropy(pw)

    result = score_password(features, shan_entropy, leaked, pw)

    print(result)

if __name__ == "__main__":
    while True:
        main()