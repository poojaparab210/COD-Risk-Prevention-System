
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
- Configurable risk thresholds
- LLM-assisted customer name and address validation
- English and Hinglish address assessment
- Mock WhatsApp confirmation and prepaid flow
- Discount calculation with configurable limits
- Explainable order-level decisions
- Interactive Streamlit dashboard
- Estimated financial impact analysis

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualisation | Matplotlib |
| Dashboard | Streamlit |
| Local LLM | Llama 3.2 (3B) |
| LLM Runtime | Ollama |
| Model Storage | Joblib |
| Configuration | JSON |
| Version Control | Git, GitHub |

## Project Structure

```text
COD-Risk-Prevention-System/
│
├── config/
│   ├── risk_thresholds.json
│   └── whatsapp_settings.json
│
├── data/
│   └── (local datasets; not committed)
│
├── models/
│   └── cod_risk_model.pkl
│
├── reports/
│   ├── eda/
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
├── requirements.txt
└── README.md
```

## Dataset Overview

The sample dataset contains historical COD order information, including:

- Customer order history
- Order value and number of items
- City, state and PIN code
- Marketing source
- Courier information
- Final delivery status

After removing duplicate order IDs and excluding one in-transit order:

- Completed orders: 1,987
- Delivered orders: 1,422
- RTO orders: 565
- Observed RTO rate: 28.43%

Customer-level source data is not included in this public repository.

## Machine Learning

Two classification algorithms were evaluated:

- Logistic Regression
- Random Forest

Logistic Regression was selected based on ROC-AUC.

| Metric | Logistic Regression |
|---|---:|
| Accuracy | 68.09% |
| Precision | 45.00% |
| Recall | 55.75% |
| F1 Score | 49.80% |
| ROC-AUC | 0.7110 |

The model provides a risk estimate, not a guarantee that an order will become RTO.

## Decision Engine

The decision engine uses configurable thresholds stored in:

`config/risk_thresholds.json`

| Predicted RTO Risk | Recommended Action |
|---|---|
| Up to 25% | Ship as-is |
| Above 25% to 45% | WhatsApp confirmation |
| Above 45% to 65% | Prepaid discount offer |
| Above 65% | Hold for manual review |

The prepaid discount is configurable, with a 5% default, a ₹20 minimum and a ₹50 maximum.

High-risk orders are held for human review rather than automatically cancelled.

## LLM-Based Address Validation

The project uses a locally hosted Llama 3.2 model through Ollama.

It assesses:
- Customer name clarity
- Address completeness
- Missing address details
- English, Hindi and Hinglish input
- Need for manual review

Python validation rules provide additional safeguards.

The current implementation was tested on 10 sample orders. It does not verify the physical existence of an address.

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

- Overall order summary
- Decision distribution
- WhatsApp simulation analysis
- Financial impact estimates
- Order-level decision logs

Financial results are estimates based on assumptions and simulated outcomes, not realised business savings.

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

For local LLM address validation, install Ollama and download the model:

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
