# def run(case):
#     """
#     Produce human-readable investigation summary
#     """
#     return {
#         "summary": "Transaction shows strong indicators of account takeover fraud.",
#         "recommendation": "Escalate for manual review",
#         "confidence": 0.82
#     }

# agents/narrative_agent.py

# def run(case):
#     behavioral = case.agent_outputs.get("behavioral", {})
#     triage = case.agent_outputs.get("triage", {})
#     pattern = case.agent_outputs.get("pattern", {})

#     deviation_score = behavioral.get("deviation_score", 0)
#     evidence = behavioral.get("evidence", [])
#     risk_level = triage.get("risk_level", "low")
#     priority = triage.get("priority", 3)
#     matched_patterns = pattern.get("matched_patterns", [])
#     pattern_confidence = pattern.get("confidence", 0.0)

#     # --- Summary ---
#     summary_parts = []

#     if matched_patterns and matched_patterns[0] != "No known fraud patterns detected":
#         summary_parts.append(
#             f"Transaction matches known fraud pattern(s): {', '.join(matched_patterns)}."
#         )
#     else:
#         summary_parts.append(
#             "No definitive known fraud pattern was matched for this transaction."
#         )

#     if deviation_score >= 70:
#         summary_parts.append(
#             "User behavior shows strong deviation from historical patterns."
#         )
#     elif deviation_score >= 40:
#         summary_parts.append(
#             "User behavior shows moderate deviation from historical patterns."
#         )
#     else:
#         summary_parts.append(
#             "User behavior is largely consistent with historical patterns."
#         )

#     summary = " ".join(summary_parts)

#     # --- Recommendation ---
#     if risk_level == "high":
#         recommendation = "Escalate for immediate manual investigation"
#     elif risk_level == "medium":
#         recommendation = "Queue for standard fraud review"
#     else:
#         recommendation = "No immediate action required; continue monitoring"

#     # --- Final Confidence ---
#     # Blend behavioral deviation + pattern confidence
#     final_confidence = round(
#         min((deviation_score / 100) * 0.6 + pattern_confidence * 0.4, 1.0),
#         2
#     )

#     return {
#         "summary": summary,
#         "recommendation": recommendation,
#         "confidence": final_confidence,
#         "priority": priority,
#         "risk_level": risk_level,
#         "supporting_evidence": evidence
#     }


# agents/narrative_agent.py

from ollama import chat


SYSTEM_PROMPT = """
You are a fraud investigation assistant at a bank.

IMPORTANT RULES:
- You do NOT decide whether a transaction is fraud.
- You do NOT change risk levels, scores, or recommendations.
- You ONLY explain and summarize the provided findings.
- If information is missing, do NOT speculate.

Write clear, professional, investigator-ready summaries.
"""


def run(case):
    behavioral = case.agent_outputs.get("behavioral", {})
    triage = case.agent_outputs.get("triage", {})
    pattern = case.agent_outputs.get("pattern", {})

    facts = {
        "deviation_score": behavioral.get("deviation_score"),
        "behavioral_evidence": behavioral.get("evidence", []),
        "risk_level": triage.get("risk_level"),
        "priority": triage.get("priority"),
        "matched_patterns": pattern.get("matched_patterns"),
        "pattern_confidence": pattern.get("confidence"),
        "recommendation": (
            "Escalate for immediate manual investigation"
            if triage.get("risk_level") == "high"
            else "Queue for standard fraud review"
            if triage.get("risk_level") == "medium"
            else "Continue monitoring"
        )
    }

    user_prompt = f"""
Summarize the following fraud investigation findings.

FACTS (DO NOT ALTER):
{facts}

OUTPUT FORMAT:
- Summary (2–3 sentences) 

Do not invent new facts.
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    narrative_text = response["message"]["content"]

    # Final confidence remains deterministic
    final_confidence = round(
        min((facts["deviation_score"] / 100) * 0.6 + facts["pattern_confidence"] * 0.4, 1.0),
        2
    )

    return {
        "summary": narrative_text,
        "recommendation": facts["recommendation"],
        "confidence": final_confidence,
        "risk_level": facts["risk_level"],
        "priority": facts["priority"],
        "supporting_evidence": facts["behavioral_evidence"]
    }