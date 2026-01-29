import hashlib
from data_loader import rockyou_hashes

def hash_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def main():
    valid = False
    
    while not valid:
        usr_pw = input("Enter a password: ").strip()
        usr_hash = hash_sha256(usr_pw)
        if usr_hash in rockyou_hashes:
            print("That is a common password")
            continue
        else:
            print("Well done! That is an uncommon password")
            valid = True

if __name__ == "__main__":
    main()