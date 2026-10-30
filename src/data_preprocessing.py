
import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "orders_sample.csv"
output_folder = project_folder / "data"


def load_data():
    if not data_file.exists():
        raise FileNotFoundError("Orders dataset was not found.")
    df = pd.read_csv(
        data_file,
        dtype={
            "phone": "string",
            "pincode": "string"
        }
    )
    print("Dataset loaded successfully!")
    print("Total rows and columns:", df.shape)
    return df


def remove_duplicates(df):
    duplicate_count = df["order_id"].duplicated().sum()
    df = df.drop_duplicates(
        subset="order_id",
        keep="first"
    ).copy()
    return df

def clean_data(df):
    text_columns = [
        "order_id",
        "customer_name",
        "address",
        "city",
        "state",
        "items",
        "utm_source",
        "courier",
        "payment_method",
        "final_status"
    ]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    df["final_status"] = df["final_status"].str.upper()
    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"],
        errors="coerce"
    )

    number_columns = [
        "order_value",
        "num_items",
        "customer_prior_orders",
        "customer_prior_rto"
    ]
    for column in number_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df["pincode"] = df["pincode"].str.replace(
        r"\.0$",
        "",
        regex=True
    )
    return df.reset_index(drop=True)


def check_missing_values(df):
    missing = df.isnull().sum()
    print("\nMissing values:")
    print(missing[missing > 0])
    print("\nTotal missing values:", missing.sum())


def get_completed_orders(df):
    completed_orders = df[
        df["final_status"].isin(["DELIVERED", "RTO"])
    ].copy()

    print("\nCompleted orders:", len(completed_orders))

    print("\nOrder status:")
    print(completed_orders["final_status"].value_counts())

    return completed_orders


def save_data(cleaned_data, completed_orders):
    output_folder.mkdir(parents=True, exist_ok=True)
    cleaned_data.to_csv(
        output_folder / "cleaned_orders.csv",
        index=False
    )

    completed_orders.to_csv(
        output_folder / "model_data.csv",
        index=False
    )

    print("\nCleaned files saved successfully!")


def main():
    orders = load_data()

    orders = remove_duplicates(orders)

    orders = clean_data(orders)
    check_missing_values(orders)

    completed_orders = get_completed_orders(orders)
    save_data(orders, completed_orders)

    print("\nData preprocessing completed!")


if __name__ == "__main__":
    main()
