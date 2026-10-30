
import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "model_data.csv"
output_folder = project_folder / "data"


def load_data():
    if not data_file.exists():
        raise FileNotFoundError(
            "Model dataset not found. Run data_preprocessing.py first."
        )

    df = pd.read_csv(data_file)
    df["is_rto"] = (
        df["final_status"].str.upper() == "RTO"
    ).astype(int)

    print("Dataset loaded successfully!")
    print("Total orders:", len(df))
    return df


def create_customer_features(df):
    df["previous_rto_rate"] = 0.0
    has_previous_orders = df["customer_prior_orders"] > 0
    df.loc[has_previous_orders, "previous_rto_rate"] = (
        df.loc[has_previous_orders, "customer_prior_rto"]
        / df.loc[has_previous_orders, "customer_prior_orders"]
    )

    df["has_previous_orders"] = (
        df["customer_prior_orders"] > 0
    ).astype(int)

    return df


def create_address_features(df):
    address = df["address"].fillna("").astype(str).str.strip()

    df["address_length"] = address.str.len()
    df["address_missing"] = (
        address == ""
    ).astype(int)

    df["pincode_missing"] = (
        df["pincode"].isna()
        | (df["pincode"].astype(str).str.strip() == "")
    ).astype(int)

    return df


def create_date_features(df):
    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"],
        errors="coerce"
    )
    df["order_month"] = df["order_datetime"].dt.month

    df["order_day"] = df["order_datetime"].dt.dayofweek

    df["is_weekend"] = (
        df["order_day"] >= 5
    ).astype(int)

    return df


def prepare_features(df):
    df = df.copy()
    df = create_customer_features(df)
    df = create_address_features(df)
    df = create_date_features(df)

    feature_columns = [
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
        "is_weekend",
        "city",
        "state",
        "utm_source",
        "courier"
    ]

    feature_data = df[["order_id"] + feature_columns + ["is_rto"]].copy()

    numerical_columns = [
        "order_value",
        "num_items",
        "customer_prior_orders",
        "customer_prior_rto",
        "previous_rto_rate",
        "address_length",
        "order_month",
        "order_day"
    ]
    for column in numerical_columns:
        feature_data[column] = pd.to_numeric(
            feature_data[column],
            errors="coerce"
        )

    feature_data = feature_data.dropna(
        subset=["is_rto"]
    )
    return feature_data

def save_features(feature_data):
    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_folder / "features.csv"

    feature_data.to_csv(
        output_file,
        index=False
    )

    print("\nFeature dataset saved successfully!")
    print("File location:", output_file)


def main():
    df = load_data()
    feature_data = prepare_features(df)
    print("\n----- Feature Engineering Results -----")

    print("Total rows:", len(feature_data))
    print("Total columns:", len(feature_data.columns))

    print("\nAvailable features:")
    print(feature_data.columns.tolist())

    print("\nMissing values:")
    print(feature_data.isnull().sum())

    save_features(feature_data)

    print("\nFeature engineering completed!")


if __name__ == "__main__":
    main()
