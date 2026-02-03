import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

DATASET_PATH = Path("data/processed/ml_data.pkl")
MODEL_OUT = Path("ml/password_model.pkl")

def main():
    print("Loading dataset...")

    with open(DATASET_PATH, "rb") as f:
        X, y = pickle.load(f)

    print(f"Total samples: {len(X)}") 

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Logistic Regression...")
    logreg = LogisticRegression(max_iter=2000)
    logreg.fit(X_train, y_train)

    preds_lr = logreg.predict(X_test)

    print("\nLogistic Regression Results:")
    print(confusion_matrix(y_test, preds_lr))
    print(classification_report(y_test, preds_lr))

    print("\nTraining Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        n_jobs=-1,
        random_state=42
    )

    rf.fit(X_train, y_train)

    preds_rf = rf.predict(X_test)

    print("\nRandom Forest Results:")
    print(confusion_matrix(y_test, preds_rf))
    print(classification_report(y_test, preds_rf))

    # Save RF
    MODEL_OUT.parent.mkdir(exist_ok=True)

    with open(MODEL_OUT, "wb") as f:
        pickle.dump(rf, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"\nSaved model to {MODEL_OUT}")

if __name__ == "__main__":
    main()