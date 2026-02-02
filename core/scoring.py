from blacklist import blacklist
from features import get_features
from entropy import shannon_entropy, policy_entropy

def get_usr_pw():
    return input("Enter a password: ").strip()

def normalise(x, low=0, high=100):
    return max(low, min(x, high))
     
def score_password(features, shan_entropy, pol_entropy, leaked):
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

    entropy = 0.7 * shan_entropy + 0.3 * pol_entropy

    if entropy < 30:
        score -= 20
        reasons.append("Entropy is low for length")
    elif entropy < 50:
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

    if features["repeated_chars"] > features["length"] * 0.4:
        score -= 10
        reasons.append("Too many repeated characters overall")

    score = normalise(score)

    if score < 20:
        label = "Very Weak"
    elif score < 40:
        label = "Weak"
    elif score < 60:
        label = "Medium"
    elif score < 80:
        label = "Strong"
    else:
        label = "Very Strong"

    if not reasons:
        reasons.append("Good length, entropy, and character variety")

    return {
        "score": score,
        "label": label,
        "entropy": round(entropy, 2),
        "reasons": reasons
    }

def main():
    pw = get_usr_pw()

    leaked = blacklist(pw)
    
    features = get_features(pw)
    shan_entropy = shannon_entropy(pw)
    pol_entropy = policy_entropy(pw)

    result = score_password(features, shan_entropy, pol_entropy, leaked)

    print(result)

if __name__ == "__main__":
    while True:
        main()