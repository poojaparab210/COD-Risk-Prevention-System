
# AI Usage Log – COD Risk Prevention System

## 1. Purpose of AI Usage

AI was used in this project to assist with reviewing customer names and delivery addresses before COD orders are shipped.

The objective was to identify potentially incomplete or unclear address information and recommend manual verification where necessary.

AI was not used for basic financial calculations or simple decision thresholds. Those tasks were handled using Python rules.

## 2. AI Technology Used

- Local LLM: Llama 3.2 (3B)
- Runtime: Ollama
- Integration: Python
- API: Local Ollama Generate API
- Output format: JSON

The model runs locally. No paid cloud LLM API is required.

## 3. Where AI Was Used

### Address Validation

The LLM receives:
- Customer name
- Delivery address
- City
- State
- PIN code

It evaluates:
- Whether the customer name appears suspicious or uncertain.
- Whether the address appears complete or incomplete.
- Whether important address details are missing.
- Whether the address uses English, Hindi, or Hinglish.
- Whether manual review is recommended.

### Why an LLM Was Used

Customer addresses can contain informal language, abbreviations, spelling variations, and Hinglish.

A fixed keyword-based system may not interpret these variations reliably. An LLM can provide contextual assessment, while Python rules control the final review decision.

## 4. Example of Weak LLM Behaviour

During initial testing, the model was asked:

"Reply with exactly one word: READY"

Expected response: READY

Actual response: YES

This demonstrated that the model did not always follow exact output instructions.

Correction:
- Use structured JSON instructions.
- Validate the returned output.
- Apply deterministic Python rules after the LLM response.
- Never depend entirely on the model's response.

## 5. Address Validation Testing

The address validator was tested on 10 sample orders.

Observed results:
- 10 orders processed.
- 6 addresses marked incomplete.
- 4 addresses marked complete.
- 6 orders recommended for manual review.
- 4 orders did not require manual review.

These results represent a small test sample and should not be treated as full-dataset validation performance.

## 6. Deterministic Safeguards

Python rules were added after the LLM assessment.

Examples:
- Suspicious customer names trigger manual review.
- Incomplete or unclear addresses trigger manual review.
- Three or more missing address details can increase the review risk level.
- Hinglish language alone does not increase risk.
- LLM uncertainty does not automatically prove fraud.

If manual review is recommended, the order is moved to the Hold / cancel review decision category.

## 7. Where AI Was Not Used

The following components use conventional Python logic or machine learning:

- Data cleaning: Pandas
- Exploratory data analysis: Pandas and Matplotlib
- Feature engineering: Python and Pandas
- RTO prediction: Scikit-learn Logistic Regression and Random Forest
- Decision thresholds: Python rules and JSON configuration
- Discount calculation: Python
- WhatsApp response simulation: Python
- Dashboard: Streamlit
- Financial estimates: Python calculations

The LLM was not used to calculate RTO costs, discounts, or financial impact.

## 8. Limitations and Risks

- The LLM cannot verify whether a physical address actually exists.
- It may misunderstand unusual names or informal address formats.
- Its output may vary between requests.
- Only 10 orders were checked during the current address-validation test.
- The model's recommendations require human review.
- No real WhatsApp messages were sent.
- Simulated customer replies do not represent actual customer behaviour.

## 9. Responsible AI Approach

The project uses AI as a supporting decision tool rather than an autonomous decision-maker.

Important safeguards:
- No automatic cancellation based only on an LLM response.
- Manual review for uncertain cases.
- Hinglish is not treated as suspicious by itself.
- Model outputs are checked using Python rules.
- Decisions and explanations are recorded in CSV logs.

## 10. Future Improvements

- Test address validation on a larger labelled dataset.
- Measure false-positive and false-negative rates.
- Improve structured output validation.
- Compare multiple local LLM models.
- Integrate an actual WhatsApp Business API.
- Collect real customer confirmation outcomes.
- Monitor model performance and financial impact over time.
