
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DECISION_FILE = BASE_DIR / "reports" / "decision_log.csv"
ADDRESS_FILE = BASE_DIR / "reports" / "address_validation.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "final_decision_log.csv"


def main():
    decisions = pd.read_csv(DECISION_FILE)
    addresses = pd.read_csv(ADDRESS_FILE)
    address_columns = addresses[
        [
            "order_id",
            "address_status",
            "risk_level",
            "manual_review",
            "reason"
        ]
    ].copy()

    final_data = decisions.merge(
        address_columns,
        on="order_id",
        how="left"
    )

    final_data["original_decision"] = final_data["decision"]

    for index, order in final_data.iterrows():

        if order["manual_review"] == True:

            final_data.at[
                index, "decision"
            ] = "Hold / cancel review"

            final_data.at[
                index, "explanation"
            ] = (
                str(order["explanation"])
                + " Address verification required: "
                + str(order["reason"])
            )

        elif pd.isna(order["manual_review"]):

            final_data.at[
                index, "address_status"
            ] = "Not checked"

    final_data.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Address validation integration completed.")

    print("\nFinal decision summary:")
    print(final_data["decision"].value_counts())

    print("\nAddress validation coverage:")
    print(
        final_data["address_status"]
        .value_counts(dropna=False)
    )

    print("\nSaved file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
