# def run(case):
#     """
#     Decide investigation priority based on alert severity & rules
#     """
#     return {
#         "risk_level": "high",
#         "priority": 1,
#         "reason": "Multiple high-risk rules triggered"
#     }


# agents/triage_agent.py

def run(case):
    """
    Assign risk and priority based on alert and behavioral deviation.
    """

    alert_severity = None
    # If we had alert severity stored in alert object, use it; fallback to rules
    if hasattr(case, "triggered_rules"):
        # simple mapping: R001 high, R002 medium, R003 medium, R004 low
        severity_map = {"R001": "high", "R002": "medium", "R003": "medium", "R004": "low"}
        severities = [severity_map.get(r, "low") for r in case.triggered_rules]
        if "high" in severities:
            alert_severity = "high"
        elif "medium" in severities:
            alert_severity = "medium"
        else:
            alert_severity = "low"

    # Behavioral score
    deviation_score = case.agent_outputs.get("behavioral", {}).get("deviation_score", 0)

    # Compute priority and risk_level
    risk_score = deviation_score
    if alert_severity == "high":
        risk_score += 20
    elif alert_severity == "medium":
        risk_score += 10

    # Cap at 100
    risk_score = min(risk_score, 100)

    # Assign risk_level
    if risk_score >= 75:
        risk_level = "high"
        priority = 1
        reason = "High deviation and/or high alert severity detected"
    elif risk_score >= 50:
        risk_level = "medium"
        priority = 2
        reason = "Moderate deviation or medium alert severity"
    else:
        risk_level = "low"
        priority = 3
        reason = "Low deviation and no high-risk alerts"

    return {
        "risk_level": risk_level,
        "priority": priority,
        "reason": reason,
        "risk_score": risk_score  # optional for analysis
    }