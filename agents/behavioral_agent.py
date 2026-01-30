# def run(case):
#     """
#     Compare transaction vs historical user behavior
#     """
#     return {
#         "deviation_score": 78,
#         "evidence": [
#             "Transaction from new country",
#             "Amount exceeds normal spending pattern"
#         ],
#         "explanation": "Behavior significantly deviates from user's historical pattern"
#     }


# agents/behavioral_agent.py

def run(case):
    transaction = case.transaction
    user = case.user_profile

    deviation_score = 0
    evidence = []

    amount = transaction["amount"]
    avg_amount = user["avg_transaction_amount"]

    country = transaction["location_country"]
    device = transaction["device_id"]
    hour = int(transaction["timestamp"][11:13])

    # 1️⃣ Amount deviation
    if amount > avg_amount * 5:
        deviation_score += 40
        evidence.append(
            f"Transaction amount ({amount}) is more than 5x user's average ({avg_amount})"
        )
    elif amount > avg_amount * 3:
        deviation_score += 25
        evidence.append(
            f"Transaction amount ({amount}) is significantly higher than user's average ({avg_amount})"
        )

    # 2️⃣ New country
    if country not in user["usual_countries"]:
        deviation_score += 25
        evidence.append(
            f"Transaction from new country ({country}); usual countries: {user['usual_countries']}"
        )

    # 3️⃣ New device
    if device not in user["usual_devices"]:
        deviation_score += 30
        evidence.append(
            "Transaction initiated from a previously unseen device"
        )

    # 4️⃣ Abnormal hour
    if hour not in user["active_hours"]:
        deviation_score += 10
        evidence.append(
            f"Transaction occurred at atypical hour ({hour}:00)"
        )

    # Cap score at 100
    deviation_score = min(deviation_score, 100)

    # Explanation
    if deviation_score >= 70:
        explanation = "Transaction behavior shows strong deviation from the user's normal spending pattern."
    elif deviation_score >= 40:
        explanation = "Transaction behavior shows moderate deviation from the user's historical activity."
    else:
        explanation = "Transaction behavior is largely consistent with the user's normal pattern."

    return {
        "deviation_score": deviation_score,
        "evidence": evidence,
        "explanation": explanation
    }

