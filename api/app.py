# api/app.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path

from orchestrator.orchestrator import FraudOrchestrator
from agents.investigator_copilot import ask
from utils.data_loader import load_all_data   # 👈 you already have this

app = FastAPI(
    title="Fraud Investigation Agent API",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def investigator_ui():
    ui_path = Path(__file__).parent.parent / "ui" / "index.html"
    return FileResponse(ui_path)

# ---- Load data ONCE ----
txn_map, user_map, alert_map = load_all_data()

# ---- Initialize orchestrator correctly ----
orchestrator = FraudOrchestrator(
    txn_map=txn_map,
    user_map=user_map,
    alert_map=alert_map
)

# In-memory case store
CASE_STORE = {}


class ChatRequest(BaseModel):
    question: str


@app.post("/investigate/{alert_id}")
def investigate_alert(alert_id: str):
    try:
        case = orchestrator.investigate(alert_id)
        CASE_STORE[alert_id] = case

        return {
            "case_id": case.case_id,
            "alert_id": case.alert_id,
            "final_verdict": case.final_verdict,
            "agent_outputs": case.agent_outputs
        }

    except KeyError:
        raise HTTPException(status_code=404, detail="Alert ID not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/investigate/{alert_id}/chat")
def chat_with_case(alert_id: str, request: ChatRequest):
    case = CASE_STORE.get(alert_id)

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found. Run investigation first."
        )

    answer = ask(case, request.question)

    return {
        "alert_id": alert_id,
        "question": request.question,
        "answer": answer
    }