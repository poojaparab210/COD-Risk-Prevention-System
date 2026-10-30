# COD Risk Prevention System

An AI-powered Cash on Delivery (COD) order risk assessment system designed to help D2C businesses identify potentially high-risk orders and reduce Return to Origin (RTO).

## Project Overview

Cash on Delivery orders can result in significant business losses when customers refuse or fail to accept deliveries.

This project analyses historical order data, predicts the probability of an order becoming RTO, and recommends an appropriate action before dispatch.

The system provides four possible decisions:
1. Ship as-is
2. Ship after WhatsApp confirmation
3. Nudge customer to prepaid with a discount
4. Hold for manual review

## Key Features

- Data preprocessing and exploratory data analysis
- Machine learning-based RTO risk prediction
- Logistic Regression and Random Forest model comparison
- Configurable risk thresholds without touching code
- LLM-assisted customer name and address validation
- English and Hinglish address assessment
- Mock WhatsApp confirmation and prepaid flow[cite: 2, 3]
- Discount calculation with configurable limits[cite: 2, 3]
- Explainable order-level decisions with plain-English reasons
- Interactive Streamlit dashboard with dedicated **Founder Morning View**
- Estimated financial impact analysis balancing RTO savings vs. Meta CAC

## Submission Deliverables

| Deliverable | File / Location | Description |
|---|---|---|
| **Codebase & Setup** | Root / `src/` | Full end-to-end Python engine, Streamlit UI, and ML models. |
| **Business Memo** | [`BUSINESS_MEMO.md`](./BUSINESS_MEMO.md) | 1–2 page executive memo written to the founder covering data findings, rules simulation, Operations vs. Marketing balance, failure modes, and roadmap. |
| **Decision Log** | [`DECISION_LOG.md`](./DECISION_LOG.md) | Running list of important architectural choices made, alternatives considered, and reasoning. |
| **AI Usage Log** | [`AI_USAGE_LOG.md`](./AI_USAGE_LOG.md) | Tools used, prompting patterns, and examples of catching and correcting weak AI outputs. |

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualisation | Altair, Matplotlib |
| Dashboard | Streamlit |
| Local LLM | Llama 3.2 (3B) |
| LLM Runtime | Ollama |
| Model Storage | Joblib |
| Configuration | JSON |
| Version Control | Git, GitHub[cite: 3] |

## Project Structure

```text
COD-Risk-Prevention-System/
│
├── config/
│   ├── risk_thresholds.json
│   └── whatsapp_settings.json
│
├── data/
│   ├── cleaned_orders.csv
│   └── (local datasets; not committed)
│
├── models/
│   └── cod_risk_model.pkl
│
├── reports/
│   ├── eda/
│   ├── final_decision_log.csv
│   ├── whatsapp_simulation.csv
│   └── model_comparison.csv
│
├── src/
│   ├── dashboard.py
│   ├── data_preprocessing.py
│   ├── eda_analysis.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── decision_engine.py
│   ├── llm_address_validator.py
│   ├── integrate_address_validation.py
│   └── whatsapp_simulator.py
│
├── .streamlit/
├── AI_USAGE_LOG.md
├── BUSINESS_MEMO.md
├── DECISION_LOG.md
├── requirements.txt
└── README.md

Dataset Overview
The sample dataset contains historical COD order information, including:

-Customer order history
-Order value and number of items[cite: 1]
-City, state and PIN code
-Marketing source
-Courier information
-Final delivery status

After removing duplicate order IDs and excluding one in-transit order:

-Completed orders: 1,987
-Delivered orders: 1,422
-RTO orders: 565
-Observed RTO rate: 28.43%[cite: 1]

Customer-level source data is not included in this public repository.

## Machine Learning
Two classification algorithms were evaluated:

-Logistic Regression
-Random Forest

Logistic Regression was selected based on ROC-AUC.

| Metric | Logistic Regression | Random Forest
|---|---|---:|
| Accuracy | 68.09% | 66.80% |
| Precision | 45.00% |42.10%|
| Recall | 55.75% |49.30%|
| F1 Score | 49.80% |45.40%|
| ROC-AUC | 0.7110 |0.6940|

The model provides a risk estimate, not a guarantee that an order will become RTO.

## Decision Engine

The decision engine uses configurable thresholds stored in:
`config/risk_thresholds.json`

| Predicted RTO Risk | Recommended Action | Operational Rationale|
|---|---|---|
| Up to 25% | Ship as-is |Low-risk orders dispatched immediately|
| Above 25% to 45% | WhatsApp confirmation |Verifies customer intent before dispatch|
| Above 45% to 65% | Prepaid discount offer |Nudges customer to convert to prepaid|
| Above 65% | Hold for manual review |Address sanity check and review before dispatch|

The prepaid discount is configurable, with a 5% default, a ₹20 minimum and a ₹50 maximum.

High-risk orders are held for human review rather than automatically cancelled to prevent wasting the ₹300 Meta acquisition cost (CAC)[cite: 1, 2].

## LLM-Based Address Validation

The project uses a locally hosted Llama 3.2 model through Ollama.

It assesses:
- Customer name clarity
- Address completeness
- Missing address details
- English, Hindi and Hinglish input
- Need for manual review

Deterministic scoring, thresholds, and financial calculations are intentionally handled in Python code rather than the LLM.

The current implementation was tested on 10 sample orders as a prototype

## WhatsApp Simulation

A mock WhatsApp workflow simulates:

- Confirmation messages
- Prepaid discount offers
- Yes, No, random and no-reply outcomes
- A 24-hour response window
- English and Hinglish messages

No real WhatsApp messages are sent.

## Dashboard

The Streamlit dashboard includes:

- Founder Morning View: A single screen displaying yesterday's orders across all 4 buckets, estimated ₹ saved from avoided RTOs, estimated ₹ lost from cancelled/held genuine orders, and net ₹ impac
- Business Overview: Decision distribution and address check statuses
- Decision Analysis: Breakdown by action tier and city.
- WhatsApp Analysis: Outcomes across customer responses and languages.
- Financial Impact: Reconciliation of RTO logistics savings (₹169.40 per order) vs. CAC loss and discount costs
- Order Logs: Searchable final decision log and simulated message history.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/poojaparab210/COD-Risk-Prevention-System.git
cd COD-Risk-Prevention-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the sample dataset

Place the provided `orders_sample.csv` file inside the `data/` directory.

The dataset is intentionally excluded from this repository because it contains customer-level information.

### 5. Run the dashboard

If the trained model and generated reports are already available:

```bash
python -m streamlit run src/dashboard.py
```

or local LLM address validation, install Ollama and download the model:

```bash
ollama pull llama3.2:3b
```
Run the dashboard in a separate terminal after starting Ollama.

## Important Limitations

- Model performance is modest and requires further validation.
- The current address validator has only been tested on 10 orders.
- WhatsApp responses are simulated.
- The source dataset contains no prepaid order examples.
- Financial impact is illustrative rather than measured.
- Human review is required for uncertain and high-risk orders.

## Future Improvements

- Validate the model using a time-based test dataset.
- Improve model calibration and threshold selection.
- Test LLM validation on a larger labelled dataset.
- Integrate WhatsApp Business API.
- Monitor real delivery and prepaid conversion outcomes.
- Improve financial impact measurement using actual operational data.

## Author

**Pooja Parab**

GitHub: https://github.com/poojaparab210

Project: https://github.com/poojaparab210/COD-Risk-Prevention-System
