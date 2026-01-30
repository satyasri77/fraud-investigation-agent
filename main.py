from utils.data_loader import load_all_data
from orchestrator.orchestrator import FraudOrchestrator
from agents.investigator_copilot import ask

if __name__ == "__main__":
    txn_map, user_map, alert_map = load_all_data("data")

    orchestrator = FraudOrchestrator(txn_map, user_map, alert_map)

    # Pick any alert ID from alerts.json
    sample_alert_id = list(alert_map.keys())[0]

    case = orchestrator.investigate(sample_alert_id)

    print("\n=== FRAUD INVESTIGATION REPORT ===")
    print("Case ID:", case.case_id)
    print("Alert ID:", case.alert_id)
    print("\nFinal Verdict:")
    print(case.final_verdict)


    print("\n--- Investigator Copilot ---\n")

    question = "Why was this transaction flagged as high risk?"
    answer = ask(case, question)

    print("Q:", question)
    print("A:", answer)