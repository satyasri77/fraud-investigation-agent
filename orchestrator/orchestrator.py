import uuid

from orchestrator.case import FraudCase
from agents import (
    triage_agent,
    behavioral_agent,
    pattern_agent,
    narrative_agent,
)


class FraudOrchestrator:

    def __init__(self, txn_map, user_map, alert_map):
        self.txn_map = txn_map
        self.user_map = user_map
        self.alert_map = alert_map

    def investigate(self, alert_id: str) -> FraudCase:
        alert = self.alert_map[alert_id]
        transaction = self.txn_map[alert["transaction_id"]]
        user = self.user_map[transaction["user_id"]]

        case = FraudCase(
            case_id=str(uuid.uuid4()),
            alert_id=alert_id,
            transaction=transaction,
            user_profile=user,
            triggered_rules=alert["triggered_rules"],
        )

        # --- Agent execution order ---
        case.agent_outputs["behavioral"] = behavioral_agent.run(case)
        case.agent_outputs["triage"] = triage_agent.run(case)
        case.agent_outputs["pattern"] = pattern_agent.run(case)
        case.final_verdict = narrative_agent.run(case)

        return case