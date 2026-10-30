# COD Risk Prevention System

An AI-powered Cash on Delivery (COD) order risk assessment engine designed for D2C brands to identify high-risk orders, prevent Return to Origin (RTO), and balance logistics savings against customer acquisition costs (CAC).

---

## Project Overview

In direct-to-consumer (D2C) e-commerce, Cash on Delivery (COD) accounts for a major portion of order volume but suffers from high Return to Origin (RTO) rates. Each RTO leads to forward and reverse freight losses, packaging waste, and inventory damage. 

However, reflexively cancelling high-risk orders burns Meta ad spend (CAC) and alienates genuine buyers. 

This project implements an end-to-end decision engine that analyzes historical COD orders, predicts RTO probability using machine learning, validates customer details and Hinglish addresses via a local LLM, and routes orders into four actionable operational buckets:

1. **Ship as-is** (Low-risk, immediate dispatch)
2. **Ship after confirmation** (WhatsApp verification for moderate risk)
3. **Nudge to prepaid** (Instant UPI payment offer with up to ₹50 discount)
4. **Hold for manual review** (High-risk or incomplete address check before release)

---

## Key Features

- **Interpretable Machine Learning:** Logistic Regression classifier calibrated on past delivery outcomes, providing explicit probabilistic risk scores.
- **Pragmatic AI Boundary:** Local Llama 3.2 (3B via Ollama) deployed strictly for unstructured tasks (Hinglish addresses, incomplete house details, fake name detection). Deterministic scoring, thresholds, and financial math are handled purely in Python.
- **No-Code Configurable Thresholds:** Risk boundaries, discount limits, and operational rules are externalized in `config/risk_thresholds.json` and `config/whatsapp_settings.json`[cite: 2].
- **WhatsApp Interaction Simulator:** Full state-machine simulation for customer confirmation flows (handling "Yes", "No", random text, and 24-hour timeout)[cite: 2].
- **Founder Morning Dashboard:** Streamlit executive view presenting the 4 bucket counts, avoided RTO savings, estimated margin/CAC foregone, and net realized financial impact.
- **Explainable Operations Output:** Every routing decision includes a concise, plain-English reason readable by warehouse and support teams[cite: 2].

---

## Submission Deliverables

As required by the assignment, all primary deliverables are documented in the repository[cite: 3]:

| Deliverable | Location | Description |
|---|---|---|
| **Codebase & Setup** | Root / `src/` | Full pipeline, ML model, LLM validator, simulator, and Streamlit app[cite: 3]. |
| **Business Memo** | [`BUSINESS_MEMO.md`](./BUSINESS_MEMO.md) | 1–2 page executive memo for the founder covering data findings, rules simulation, Operations vs Marketing ₹ balance, failure modes, and roadmap[cite: 3]. |
| **Decision Log** | [`DECISION_LOG.md`](./DECISION_LOG.md) | Running list of design choices, rejected alternatives, and justifications[cite: 3]. |
| **AI Usage Log** | [`AI_USAGE_LOG.md`](./AI_USAGE_LOG.md) | Tools used, prompting patterns, and examples of catching and correcting weak AI outputs[cite: 3]. |

---

## Financial Framework & Unit Economics

Decisions and threshold gates are anchored in unit economics rather than arbitrary assumptions:

- **Forward Shipping:** ₹65[cite: 1]
- **Return Shipping:** ₹65[cite: 1]
- **Packaging & Handling:** ₹25[cite: 1]
- **Unresellable Damage:** 8% damage rate on average ₹180 product cost = ₹14.40[cite: 1]
- **Direct Sunk Cost per RTO:** **₹169.40**[cite: 1]
- **Average Order Value (AOV):** ₹649[cite: 1]
- **Gross Margin on Delivered Order:** 62% (₹402.38 gross margin per delivered order)[cite: 1]
- **Customer Acquisition Cost (CAC):** ₹300+ spent via Meta Ads[cite: 2]
- **Breakeven Cancellation Risk:** 
  $$\text{Threshold} = \frac{\text{RTO Cost}}{\text{Gross Margin} + \text{CAC}} = \frac{₹169.40}{₹402.38 + ₹300.00} \approx 24.1\% \text{ delivery probability (75.9\% failure risk)}$$
  *(An order is only held/cancelled if its chance of non-delivery outweighs the ₹702.38 sunk cost of losing an authentic customer[cite: 1, 2].)*

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Joblib |
| Visualisation | Altair, Matplotlib |
| Application & Dashboard | Streamlit |
| Local LLM Runtime | Llama 3.2 (3B) via Ollama |
| Configuration Management | JSON |
| Version Control | Git, GitHub |

---

## Project Structure

```text
COD-Risk-Prevention-System/
│
├── config/
│   ├── risk_thresholds.json          # Configurable risk cutoffs and action buckets
│   └── whatsapp_settings.json        # Messaging timeouts, discount limits, and copy
│
├── data/
│   ├── cleaned_orders.csv            # Cleaned orders dataset
│   └── (orders_sample.csv local)     # Raw order sample
│
├── models/
│   └── cod_risk_model.pkl            # Trained Logistic Regression model
│
├── reports/
│   ├── final_decision_log.csv        # Evaluated decisions and plain-English reasons
│   ├── whatsapp_simulation.csv       # Message delivery and customer reply log
│   └── model_comparison.csv          # Algorithm benchmark metrics
│
├── src/
│   ├── dashboard.py                  # Streamlit founder & operations dashboard
│   ├── data_preprocessing.py         # Data cleaning and sanity checks
│   ├── eda_analysis.py               # Exploratory data analysis scripts
│   ├── feature_engineering.py        # Feature extraction and encoding
│   ├── train_model.py                # Model training, calibration, and evaluation
│   ├── decision_engine.py            # 4-tier decision routing and threshold logic
│   ├── llm_address_validator.py      # Ollama/Llama 3.2 address parsing & Hinglish sanitization
│   ├── integrate_address_validation.py# Pipeline connecting ML score with LLM validation
│   └── whatsapp_simulator.py         # WhatsApp state-machine simulator
│
├── .streamlit/                       # Streamlit UI configuration
├── AI_USAGE_LOG.md                   # AI usage documentation & failure corrections
├── BUSINESS_MEMO.md                  # Executive memo for company leadership
├── DECISION_LOG.md                   # Architectural choices and trade-offs log
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation and setup guide

Author
Pooja Parab
GitHub: https://github.com/poojaparab210
Project: https://github.com/poojaparab210/COD-Risk-Prevention-System
