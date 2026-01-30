# agents/investigator_copilot.py

from ollama import chat

SYSTEM_PROMPT = """
You are a Fraud Investigation Copilot assisting a human investigator.

STRICT RULES:
- You do NOT decide fraud outcomes.
- You do NOT change risk levels, confidence, or recommendations.
- You ONLY answer using the provided case information.
- If a question cannot be answered from the data, say so clearly.
- Be concise, professional, and investigator-focused.
"""


def build_case_context(case):
    """
    Convert case + agent outputs into a readable context for the LLM.
    """
    context = f"""
CASE ID: {case.case_id}
ALERT ID: {case.alert_id}

TRANSACTION:
{case.transaction}

TRIGGERED RULES:
{case.triggered_rules}

BEHAVIORAL ANALYSIS:
{case.agent_outputs.get("behavioral")}

TRIAGE ASSESSMENT:
{case.agent_outputs.get("triage")}

PATTERN ANALYSIS:
{case.agent_outputs.get("pattern")}

FINAL VERDICT:
{case.final_verdict}
"""
    return context


def ask(case, question: str) -> str:
    case_context = build_case_context(case)

    user_prompt = f"""
You are reviewing the following fraud case.

CASE DETAILS:
{case_context}

INVESTIGATOR QUESTION:
{question}

Answer clearly using ONLY the case details above.
Do not hallucilnate 
Do not consider any content outside the case details
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response["message"]["content"]