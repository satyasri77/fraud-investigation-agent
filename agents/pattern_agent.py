# def run(case):
#     """
#     Match transaction against known fraud patterns
#     """
#     return {
#         "matched_patterns": ["Account Takeover"],
#         "confidence": 0.81
#     }


# agents/pattern_agent.py

def run(case):
    """
    Detect known fraud patterns based on combined agent outputs and triggered rules.
    """

    patterns = []
    confidence = 0.0

    deviation_score = case.agent_outputs.get("behavioral", {}).get("deviation_score", 0)
    risk_level = case.agent_outputs.get("triage", {}).get("risk_level", "low")
    triggered_rules = case.triggered_rules

    # --- Pattern 1: Account Takeover (ATO) ---
    # High deviation + new device + new country + high-risk rule
    if deviation_score >= 70 and "R001" in triggered_rules and "R003" in triggered_rules:
        patterns.append("Account Takeover")
        confidence += 0.6

    # --- Pattern 2: Transaction Velocity Fraud ---
    # Multiple failed transactions or many high-value transactions in 24h
    if "R001" in triggered_rules and deviation_score >= 50:
        patterns.append("Transaction Velocity Fraud")
        confidence += 0.4

    # --- Pattern 3: Card Not Present (CNP) Fraud ---
    # Online merchant + high deviation + medium-risk rule
    online_merchants = ["Amazon", "Flipkart", "Netflix", "Swiggy", "Zomato"]
    if case.transaction["merchant_name"] in online_merchants and deviation_score >= 60:
        patterns.append("Card Not Present Fraud")
        confidence += 0.3

    # Normalize confidence
    confidence = min(confidence, 1.0)

    if not patterns:
        patterns.append("No known fraud patterns detected")
        confidence = 0.0

    return {
        "matched_patterns": patterns,
        "confidence": round(confidence, 2)
    }