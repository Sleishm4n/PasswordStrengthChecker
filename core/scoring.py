from blacklist import blacklist
from features import get_features

def get_usr_pw():
    return input("Enter a password: ").strip()
     

def main():
    pw = get_usr_pw()

    leaked = blacklist(pw)
    
    features = get_features(pw)

    print(features)

if __name__ == "__main__":
    main()