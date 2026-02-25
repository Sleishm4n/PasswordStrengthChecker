from collections import Counter
import math

def policy_entropy(password):
    total_p = 0

    if any(c.islower() for c in password):
        total_p += 26
    if any(c.isupper() for c in password):
        total_p += 26
    if any(c.isdigit() for c in password):
        total_p += 10
    if any(not c.isalnum() for c in password):
        total_p += 32

    if total_p == 0:
        return 0
    
    return len(password) * math.log2(total_p)

def shannon_entropy(password):
    counts = Counter(password)
    n = len(password)

    entropy = 0
    for c in counts.values():
        p = c / n
        entropy -= p * math.log2(p)

    return entropy
