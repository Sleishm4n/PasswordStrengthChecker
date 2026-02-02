import hashlib
from hash_data_loader import rockyou_contains

def hash_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def blacklist(password):
    return rockyou_contains(hash_sha256(password))

def main():  
    while True:
        usr_pw = input("Enter a password: ")
        if blacklist(usr_pw):
            print("That is a common password")
        else:
            print("Well done! That is an uncommon password")
            break

if __name__ == "__main__":
    main()