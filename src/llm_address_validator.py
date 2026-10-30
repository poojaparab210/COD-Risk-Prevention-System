
import pandas as pd
import json
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned_orders.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "address_validation.csv"

MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

MAX_ORDERS = 10


def validate_address(order):

    prompt = f"""
You are an address quality assistant for an Indian e-commerce company.

Review the complete delivery information.

Customer name: {order['customer_name']}
Address: {order['address']}
City: {order['city']}
State: {order['state']}
Pincode: {order['pincode']}

Important rules:
- Evaluate address, city, state and pincode together.
- The city may be provided separately from the address field.
- Understand English, Hindi and Hinglish.
- Hinglish is a valid way of writing an Indian address.
- Never mark an address suspicious only because it uses Hinglish.
- A full state name is acceptable.
- Do not require a country name or state abbreviation.
- Do not claim that an address physically exists.
- Do not assume a name is fake without clear evidence.
- A missing landmark alone does not mean an address is invalid.

Evaluate:
1. Name quality.
2. Address completeness.
3. Whether the complete delivery information is understandable.
4. Whether manual verification is needed.

Return only valid JSON:

{{
    "name_status": "normal or suspicious or uncertain",
    "address_status": "complete or incomplete or unclear",
    "language": "English or Hinglish or mixed or unknown",
    "missing_details": [],
    "reason": "short explanation"
}}
"""

    request_data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(request_data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        validation = json.loads(result["response"])

        required_fields = [
            "name_status",
            "address_status",
            "language",
            "missing_details",
            "reason"
        ]

        for field in required_fields:
            if field not in validation:
                raise ValueError(f"Missing field: {field}")

        if not isinstance(validation["missing_details"], list):
            validation["missing_details"] = []

        return validation

    except Exception as error:

        return {
            "name_status": "unknown",
            "address_status": "unclear",
            "language": "unknown",
            "missing_details": [],
            "reason": f"LLM validation failed: {error}"
        }


def apply_review_rules(validation):

    name_status = str(
        validation["name_status"]
    ).lower()

    address_status = str(
        validation["address_status"]
    ).lower()

    missing_details = validation["missing_details"]

    # Default risk and review decision
    risk_level = "low"
    manual_review = False

    # Suspicious names require manual verification
    if name_status == "suspicious":
        risk_level = "high"
        manual_review = True

    # Incomplete or unclear addresses need review
    elif address_status in ["incomplete", "unclear"]:
        manual_review = True

        if len(missing_details) >= 3:
            risk_level = "high"
        else:
            risk_level = "medium"

    # Uncertain names also need verification
    elif name_status == "uncertain":
        risk_level = "medium"
        manual_review = True

    return risk_level, manual_review


def main():

    orders = pd.read_csv(
        INPUT_FILE,
        dtype={
            "phone": str,
            "pincode": str
        }
    )

    sample_orders = orders.head(MAX_ORDERS)

    results = []

    print("Starting local LLM address validation...")

    for _, order in sample_orders.iterrows():

        print(f"Checking order: {order['order_id']}")

        validation = validate_address(order)

        risk_level, manual_review = apply_review_rules(
            validation
        )

        results.append({
            "order_id": order["order_id"],
            "customer_name": order["customer_name"],
            "address": order["address"],
            "city": order["city"],
            "pincode": order["pincode"],
            "name_status": validation["name_status"],
            "address_status": validation["address_status"],
            "language": validation["language"],
            "missing_details": json.dumps(
                validation["missing_details"]
            ),
            "risk_level": risk_level,
            "manual_review": manual_review,
            "reason": validation["reason"]
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nAddress validation completed.")
    print("Orders checked:", len(results_df))

    print("\nRisk level summary:")
    print(results_df["risk_level"].value_counts())

    print("\nManual review summary:")
    print(results_df["manual_review"].value_counts())

    print("\nSaved results:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
