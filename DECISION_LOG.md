# Engineering & Architecture Decision Log

### 1. Algorithm Selection: Logistic Regression vs. Random Forest
* **Options Considered:** Logistic Regression, Random Forest Classifier, XGBoost.
* **Choice Made:** Logistic Regression.
* **Why:** While Random Forest achieved slightly higher training accuracy, Logistic Regression delivered well-calibrated probabilities (ROC-AUC: 0.711) and clear coefficient explainability. In an operations setting, knowing exactly which features increase risk is critical for generating plain-English reasons.

### 2. LLM Boundary: Local Llama 3.2 (3B) vs. Cloud LLMs vs. Pure Heuristics
* **Options Considered:** OpenAI GPT-4o API, pure Regex heuristics, local Llama 3.2 via Ollama.
* **Choice Made:** Local Llama 3.2 (3B) restricted strictly to customer name sanity and address completeness/Hinglish parsing.
* **Why:** Cloud APIs introduce per-order costs and data privacy concerns with customer addresses. Pure regex cannot reliably parse Hinglish phrases (e.g., "Gali no 3, near temple, kirana store ke samne"). Using a 3B model locally keeps operational cost at zero while handling messy colloquial Indian addresses.

### 3. Action Strategy: "Hold for Manual Review" vs. "Auto-Cancel"
* **Options Considered:** Automatically cancelling any order with risk > 65%.
* **Choice Made:** Placed high-risk orders in a "Hold for Review / Verification" queue.
* **Why:** Sunk acquisition cost (Meta CAC ₹300+) and gross margin (₹402.38) mean that cancelling a genuine customer causes an asymmetric ₹702 loss versus an avoided ₹169 RTO cost. Outright cancellation should be reserved only for confirmed fraud/bot activity.

### 4. Prepaid Discount Structure: Dynamic 5% (Min ₹20 / Max ₹50)
* **Options Considered:** Flat 10% discount, flat ₹100 discount, ₹50 flat discount.
* **Choice Made:** 5% cart value discount with a ₹20 floor and a ₹50 ceiling.
* **Why:** On orders above ₹1,000, unconstrained percentage discounts erode gross margin unnecessarily. A ₹50 cap provides sufficient incentive to drive UPI conversion while preserving contribution margin and remaining far below the ₹169.40 RTO cost.