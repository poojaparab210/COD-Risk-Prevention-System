import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

data_file = project_folder / "data" / "model_data.csv"
output_folder = project_folder / "reports" / "eda"


def load_data():
    if not data_file.exists():
        raise FileNotFoundError(
            "Dataset not found. Run data_preprocessing.py first."
        )
    df = pd.read_csv(data_file)

    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"],
        errors="coerce"
    )

    df["is_rto"] = (df["final_status"] == "RTO").astype(int)

    print("Dataset loaded successfully!")
    print("Total orders:", len(df))
    return df


def calculate_rto_rate(data, group_column):
    result = data.groupby(group_column).agg(
        total_orders=("is_rto", "count"),
        rto_orders=("is_rto", "sum"),
        rto_rate=("is_rto", "mean")
    ).reset_index()

    result["rto_rate"] = result["rto_rate"] * 100

    return result


def calculate_overall_rto(df):
    total_orders = len(df)
    rto_orders = df["is_rto"].sum()
    delivered_orders = total_orders - rto_orders

    rto_rate = (rto_orders / total_orders) * 100

    print("\n----- Overall RTO Analysis -----")
    print("Total orders:", total_orders)
    print("RTO orders:", rto_orders)
    print("Delivered orders:", delivered_orders)
    print(f"Overall RTO rate: {rto_rate:.2f}%")


def analyse_customer_history(df):
    result = calculate_rto_rate(
        df,
        "customer_prior_rto"
    )

    print("\n----- Customer History Analysis -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "customer_history_analysis.csv",
        index=False
    )


def analyse_marketing_source(df):
    result = calculate_rto_rate(
        df,
        "utm_source"
    )

    result = result.sort_values(
        "rto_rate",
        ascending=False
    )

    print("\n----- Marketing Source Analysis -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "marketing_analysis.csv",
        index=False
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        result["utm_source"],
        result["rto_rate"]
    )

    plt.title("RTO Rate by Marketing Source")
    plt.xlabel("Marketing Source")
    plt.ylabel("RTO Rate (%)")
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    plt.savefig(output_folder / "marketing_rto.png")
    plt.close()


def analyse_courier(df):
    result = calculate_rto_rate(
        df,
        "courier"
    )

    result = result.sort_values(
        "rto_rate",
        ascending=False
    )

    print("\n----- Courier Analysis -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "courier_analysis.csv",
        index=False
    )


def analyse_city(df):
    """Find cities with higher RTO percentages."""

    result = calculate_rto_rate(
        df,
        "city"
    )

    result = result[result["total_orders"] >= 20]

    result = result.sort_values(
        "rto_rate",
        ascending=False
    )

    print("\n----- City-wise RTO Analysis -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "city_analysis.csv",
        index=False
    )


def analyse_order_value(df):
    df = df.copy()
    price_ranges = [
        -1, 300, 500, 700, 1000, 1500, 2000, float("inf")
    ]

    range_names = [
        "0-300",
        "301-500",
        "501-700",
        "701-1000",
        "1001-1500",
        "1501-2000",
        "Above 2000"
    ]

    df["order_value_range"] = pd.cut(
        df["order_value"],
        bins=price_ranges,
        labels=range_names
    )

    result = calculate_rto_rate(
        df,
        "order_value_range"
    )

    print("\n----- Order Value Analysis -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "order_value_analysis.csv",
        index=False
    )


def analyse_monthly_trend(df):
    df = df.copy()
    df["month"] = df["order_datetime"].dt.to_period("M")

    result = calculate_rto_rate(
        df,
        "month"
    )

    result["month"] = result["month"].astype(str)

    print("\n----- Monthly RTO Trend -----")
    print(result.round(2))

    result.to_csv(
        output_folder / "monthly_analysis.csv",
        index=False
    )
    plt.figure(figsize=(9, 5))

    plt.plot(
        result["month"],
        result["rto_rate"],
        marker="o"
    )

    plt.title("Monthly RTO Rate")
    plt.xlabel("Month")
    plt.ylabel("RTO Rate (%)")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig(output_folder / "monthly_rto.png")
    plt.close()


def main():
    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )
    df = load_data()

    calculate_overall_rto(df)
    analyse_customer_history(df)
    analyse_marketing_source(df)
    analyse_courier(df)
    analyse_city(df)
    analyse_order_value(df)
    analyse_monthly_trend(df)

    print("\nEDA completed successfully!")
    print("Reports saved in:", output_folder)


if __name__ == "__main__":
    main()
