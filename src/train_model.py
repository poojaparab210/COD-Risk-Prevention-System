
import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)


project_folder = Path(__file__).resolve().parent.parent

data_file = project_folder / "data" / "features.csv"
model_folder = project_folder / "models"
report_folder = project_folder / "reports"

numerical_features = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto",
    "previous_rto_rate",
    "has_previous_orders",
    "address_length",
    "address_missing",
    "pincode_missing",
    "order_month",
    "order_day",
    "is_weekend"
]

categorical_features = [
    "city",
    "state",
    "utm_source",
    "courier"
]


def load_data():
    if not data_file.exists():
        raise FileNotFoundError(
            "Feature dataset not found. Run feature_engineering.py first."
        )
    df = pd.read_csv(data_file)

    print("Feature dataset loaded successfully!")
    print("Total orders:", len(df))
    return df

def prepare_data(df):
    X = df[numerical_features + categorical_features]
    y = df["is_rto"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining orders:", len(X_train))
    print("Testing orders:", len(X_test))

    return X_train, X_test, y_train, y_test

def create_preprocessor(scale_numbers=True):
    if scale_numbers:
        numerical_steps = [
            ("fill_missing", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    else:
        numerical_steps = [
            ("fill_missing", SimpleImputer(strategy="median"))
        ]

    numerical_pipeline = Pipeline(
        steps=numerical_steps
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("fill_missing", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numbers", numerical_pipeline, numerical_features),
            ("categories", categorical_pipeline, categorical_features)
        ]
    )

    return preprocessor


def train_logistic_regression(X_train, y_train):
    model = Pipeline(
        steps=[
            ("preprocessing", create_preprocessor(scale_numbers=True)),
            ("classifier", LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            ))
        ]
    )

    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    model = Pipeline(
        steps=[
            ("preprocessing", create_preprocessor(scale_numbers=False)),
            ("classifier", RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                class_weight="balanced",
                random_state=42
            ))
        ]
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test, model_name):
    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    roc_auc = roc_auc_score(y_test, probabilities)

    print(f"\n----- {model_name} Results -----")

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Delivered", "RTO"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return {
        "model_name": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc
    }


def main():
    model_folder.mkdir(parents=True, exist_ok=True)
    report_folder.mkdir(parents=True, exist_ok=True)

    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)

    print("\nTraining Logistic Regression...")
    logistic_model = train_logistic_regression(X_train, y_train)

    print("Training Random Forest...")
    random_forest_model = train_random_forest(X_train, y_train)

    logistic_results = evaluate_model(
        logistic_model,
        X_test,
        y_test,
        "Logistic Regression"
    )

    random_forest_results = evaluate_model(
        random_forest_model,
        X_test,
        y_test,
        "Random Forest"
    )

    results = pd.DataFrame([
        logistic_results,
        random_forest_results
    ])

    results = results.sort_values(
        by="roc_auc",
        ascending=False
    )

    print("\n----- Model Comparison -----")
    print(results.round(4).to_string(index=False))

    results.to_csv(
        report_folder / "model_comparison.csv",
        index=False
    )

    if logistic_results["roc_auc"] >= random_forest_results["roc_auc"]:
        best_model = logistic_model
        best_model_name = "Logistic Regression"
    else:
        best_model = random_forest_model
        best_model_name = "Random Forest"

    model_file = model_folder / "cod_risk_model.pkl"

    joblib.dump(best_model, model_file)

    print("\nSelected model:", best_model_name)
    print("Model saved at:", model_file)

    print("\nModel training completed successfully!")


if __name__ == "__main__":
    main()
