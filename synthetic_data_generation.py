import random
import uuid
import json
from datetime import datetime, timedelta

# -------------------------
# CONFIG
# -------------------------
NUM_USERS = 1000
MAX_TXNS_PER_USER = 60
FRAUD_PROBABILITY = 0.1

COUNTRIES = ["IN", "US", "SG", "AE", "GB"]
MERCHANTS = [
    ("Amazon", "ELECTRONICS"),
    ("Flipkart", "ELECTRONICS"),
    ("Swiggy", "FOOD"),
    ("Zomato", "FOOD"),
    ("Uber", "TRANSPORT"),
    ("IRCTC", "TRAVEL"),
    ("Netflix", "ENTERTAINMENT"),
]

CHANNELS = ["card", "upi", "netbanking"]

# -------------------------
# FRAUD RULES
# -------------------------
fraud_rules = [
    {
        "rule_id": "R001",
        "rule_name": "High Amount Deviation",
        "description": "Transaction amount > 5x user average",
        "severity": "high",
    },
    {
        "rule_id": "R002",
        "rule_name": "New Country",
        "description": "Transaction from unseen country",
        "severity": "medium",
    },
    {
        "rule_id": "R003",
        "rule_name": "New Device",
        "description": "Transaction from unseen device",
        "severity": "medium",
    },
    {
        "rule_id": "R004",
        "rule_name": "Abnormal Hour",
        "description": "Transaction outside normal active hours",
        "severity": "low",
    },
]

# -------------------------
# DATA CONTAINERS
# -------------------------
users = []
transactions = []
alerts = []

# -------------------------
# GENERATE USERS
# -------------------------
for i in range(NUM_USERS):
    user_id = f"U{i:04d}"
    avg_amt = random.randint(500, 3000)
    max_amt = avg_amt * random.randint(3, 6)
    device_id = f"DEV_{uuid.uuid4().hex[:6]}"

    profile = {
        "user_id": user_id,
        "account_age_days": random.randint(180, 3000),
        "avg_transaction_amount": avg_amt,
        "max_transaction_amount": max_amt,
        "usual_countries": ["IN"],
        "usual_devices": [device_id],
        "preferred_merchants": random.sample([m[0] for m in MERCHANTS], 3),
        "active_hours": list(range(8, 22)),
        "transactions_last_30d": random.randint(15, 60),
        "failed_transactions_last_30d": random.randint(0, 2),
    }

    users.append(profile)

# -------------------------
# GENERATE TRANSACTIONS
# -------------------------
txn_counter = 100000
alert_counter = 900000

for user in users:
    num_txns = random.randint(20, MAX_TXNS_PER_USER)

    for _ in range(num_txns):
        is_fraud_like = random.random() < FRAUD_PROBABILITY
        merchant, category = random.choice(MERCHANTS)

        amount = (
            random.randint(
                user["avg_transaction_amount"],
                user["max_transaction_amount"],
            )
            if not is_fraud_like
            else user["avg_transaction_amount"] * random.randint(6, 10)
        )

        location = (
            random.choice(user["usual_countries"])
            if not is_fraud_like
            else random.choice([c for c in COUNTRIES if c not in user["usual_countries"]])
        )

        device = (
            random.choice(user["usual_devices"])
            if not is_fraud_like
            else f"DEV_{uuid.uuid4().hex[:6]}"
        )

        hour = (
            random.choice(user["active_hours"])
            if not is_fraud_like
            else random.choice([0, 1, 2, 3, 4])
        )

        timestamp = (
            datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ).replace(hour=hour)

        txn_id = f"TXN{txn_counter}"
        txn_counter += 1

        txn = {
            "transaction_id": txn_id,
            "user_id": user["user_id"],
            "amount": amount,
            "currency": "INR",
            "merchant_name": merchant,
            "merchant_category": category,
            "location_country": location,
            "device_id": device,
            "channel": random.choice(CHANNELS),
            "timestamp": timestamp.isoformat(),
            "status": "approved",
        }

        transactions.append(txn)

        # -------------------------
        # RULE EVALUATION
        # -------------------------
        triggered = []

        if amount > user["avg_transaction_amount"] * 5:
            triggered.append("R001")

        if location not in user["usual_countries"]:
            triggered.append("R002")

        if device not in user["usual_devices"]:
            triggered.append("R003")

        if hour not in user["active_hours"]:
            triggered.append("R004")

        if triggered:
            alert = {
                "alert_id": f"ALERT{alert_counter}",
                "transaction_id": txn_id,
                "triggered_rules": triggered,
                "alert_severity": (
                    "high"
                    if "R001" in triggered
                    else "medium"
                    if len(triggered) > 1
                    else "low"
                ),
                "created_at": datetime.utcnow().isoformat(),
            }
            alert_counter += 1
            alerts.append(alert)

# -------------------------
# WRITE FILES
# -------------------------
with open("data/user_profiles.json", "w") as f:
    json.dump(users, f, indent=2)

with open("data/transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

with open("data/fraud_rules.json", "w") as f:
    json.dump(fraud_rules, f, indent=2)

with open("data/alerts.json", "w") as f:
    json.dump(alerts, f, indent=2)

print("✅ Synthetic fraud investigation data generated successfully!")
print(f"Users: {len(users)}")
print(f"Transactions: {len(transactions)}")
print(f"Alerts: {len(alerts)}")