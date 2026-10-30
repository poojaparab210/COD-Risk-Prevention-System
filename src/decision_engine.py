
import pandas as pd
import joblib
import json

from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

data_file = project_folder / "data" / "features.csv"
model_file = project_folder / "models" / "cod_risk_model.pkl"
config_file = project_folder / "config" / "risk_thresholds.json"

output_folder = project_folder / "reports"


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

feature_columns = numerical_features + categorical_features


def load_files():
    if not data_file.exists():
        raise FileNotFoundError(
            "Feature data not found. Run feature_engineering.py first."
        )

    if not model_file.exists():
        raise FileNotFoundError(
            "Trained model not found. Run train_model.py first."
        )

    if not config_file.exists():
        raise FileNotFoundError(
            "Risk settings not found. Check config/risk_thresholds.json."
        )

    df = pd.read_csv(data_file)

    model = joblib.load(model_file)

    with open(config_file, "r") as file:
        settings = json.load(file)

    print("Model, data and settings loaded successfully!")

    return df, model, settings


def calculate_discount(order_value, settings):
    discount_percent = settings["prepaid_discount_percent"]
    discount = order_value * discount_percent / 100
    discount = max(
        discount,
        settings["minimum_discount"]
    )

    discount = min(
        discount,
        settings["maximum_discount"]
    )

    return round(discount, 2)


def make_decision(risk_probability, order_value, settings):
    ship_limit = settings["ship_as_is_max"]
    confirmation_limit = settings["confirmation_max"]
    prepaid_limit = settings["prepaid_max"]

    if risk_probability <= ship_limit:

        decision = "Ship as-is"
        discount = 0

        explanation = (
            "The predicted RTO risk is low. "
            "The order can be shipped without additional confirmation."
        )

    elif risk_probability <= confirmation_limit:

        decision = "Ship after WhatsApp confirmation"
        discount = 0

        explanation = (
            "The predicted RTO risk is moderate. "
            "Confirm the order with the customer before shipping."
        )

    elif risk_probability <= prepaid_limit:

        decision = "Nudge to prepaid"
        discount = calculate_discount(
            order_value,
            settings
        )

        explanation = (
            "The predicted RTO risk is high. "
            "Offer a prepaid payment option with a discount."
        )

    else:

        decision = "Hold / cancel review"
        discount = 0

        explanation = (
            "The predicted RTO risk is very high. "
            "Hold the order for manual review before taking action. "
            "Do not automatically cancel it based only on the model score."
        )

    return decision, discount, explanation


def process_orders(df, model, settings):
    X = df[feature_columns].copy()
    risk_probabilities = model.predict_proba(X)[:, 1]

    decision_records = []

    for index, risk_probability in enumerate(risk_probabilities):

        order_value = df.iloc[index]["order_value"]

        decision, discount, explanation = make_decision(
            risk_probability,
            order_value,
            settings
        )

        decision_records.append({
            "order_id": df.iloc[index]["order_id"],
            "order_value": order_value,
            "rto_risk_percent": round(
                risk_probability * 100,
                2
            ),
            "decision": decision,
            "prepaid_discount": discount,
            "explanation": explanation
        })

    return pd.DataFrame(decision_records)


def save_decisions(decisions):
    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_folder / "decision_log.csv"

    decisions.to_csv(
        output_file,
        index=False
    )

    print("\nDecision log saved successfully!")
    print("File location:", output_file)


def main():
    df, model, settings = load_files()
    decisions = process_orders(
        df,
        model,
        settings
    )
    print("\n----- Order Decision Summary -----")

    print(
        decisions["decision"].value_counts()
    )
    print("\n----- Sample Decisions -----")

    print(
        decisions.head(10).to_string(index=False)
    )
    save_decisions(decisions)

    print("\nDecision engine completed successfully!")


if __name__ == "__main__":
    main()
