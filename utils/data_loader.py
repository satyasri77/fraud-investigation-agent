import json


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def load_all_data(data_dir="data"):
    transactions = load_json(f"{data_dir}/transactions.json")
    users = load_json(f"{data_dir}/user_profiles.json")
    alerts = load_json(f"{data_dir}/alerts.json")

    txn_map = {t["transaction_id"]: t for t in transactions}
    user_map = {u["user_id"]: u for u in users}
    alert_map = {a["alert_id"]: a for a in alerts}

    return txn_map, user_map, alert_map