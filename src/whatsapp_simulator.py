
import pandas as pd
import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DECISION_FILE = BASE_DIR / "reports" / "final_decision_log.csv"
SETTINGS_FILE = BASE_DIR / "config" / "whatsapp_settings.json"
OUTPUT_FILE = BASE_DIR / "reports" / "whatsapp_simulation.csv"


def load_settings():
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def create_message(decision, language, discount):

    if decision == "Ship after WhatsApp confirmation":

        if language == "English":
            return (
                "Hello! Please confirm your COD order. "
                "Reply YES to confirm or NO to cancel."
            )

        return (
            "Namaste! Aapka COD order confirm karein. "
            "Confirm karne ke liye YES ya cancel karne ke liye NO reply karein."
        )

    if decision == "Nudge to prepaid":

        if language == "English":
            return (
                f"Pay online and get ₹{discount:.0f} discount "
                "on your order. Reply YES to accept."
            )

        return (
            f"Online payment karne par aapko ₹{discount:.0f} "
            "discount milega. Accept karne ke liye YES reply karein."
        )

    return ""


def simulate_reply(probabilities):

    reply_types = list(probabilities.keys())
    reply_weights = list(probabilities.values())

    return random.choices(
        reply_types,
        weights=reply_weights,
        k=1
    )[0]


def process_response(decision, reply):

    if decision == "Ship after WhatsApp confirmation":

        if reply == "yes":
            return "COD Confirmed - Ship"

        if reply == "no":
            return "Customer Cancelled"

        if reply == "random":
            return "Manual Follow-up Required"

        return "No Reply - Hold for Review"

    if decision == "Nudge to prepaid":

        if reply == "yes":
            return "Prepaid Accepted - Ship"

        if reply == "no":
            return "Prepaid Declined - COD Review"

        if reply == "random":
            return "Manual Follow-up Required"

        return "No Reply - Hold for Review"

    return "No WhatsApp Message"


def main():

    random.seed(42)

    settings = load_settings()
    orders = pd.read_csv(DECISION_FILE)

    results = []

    message_decisions = [
        "Ship after WhatsApp confirmation",
        "Nudge to prepaid"
    ]

    for _, order in orders.iterrows():

        decision = order["decision"]

        # Only send messages for eligible decisions
        if decision not in message_decisions:
            continue

        discount = order["prepaid_discount"]

        language = random.choice(settings["languages"])

        message = create_message(
            decision,
            language,
            discount
        )

        reply = simulate_reply(
            settings["reply_probabilities"]
        )

        outcome = process_response(
            decision,
            reply
        )

        results.append({
            "order_id": order["order_id"],
            "decision": decision,
            "language": language,
            "message": message,
            "reply": reply,
            "response_window_hours": settings["response_window_hours"],
            "simulated_outcome": outcome,
            "discount": discount
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("WhatsApp simulation completed.")

    print("Total messages simulated:", len(results_df))

    print("\nOrders not sent WhatsApp messages:")
    print(len(orders) - len(results_df))

    print("\nSimulated customer replies:")

    if not results_df.empty:
        print(results_df["reply"].value_counts())

        print("\nSimulated outcomes:")
        print(results_df["simulated_outcome"].value_counts())

    print("\nSaved file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
