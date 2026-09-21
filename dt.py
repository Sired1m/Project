"""
Generates fresh meds.csv and intake_log.csv for testing, with all timestamps
computed relative to the moment this script is run - so nothing goes "stale"
no matter when you actually test.

Covers both filters:
  schedule_builder:     next_intake_time >= now - 30min, <= now + 24h, stock >= pills_per_dose
  list_not_taken_meds:  next_intake_time + 30min < now

Run this right before opening the Streamlit app:
    python generate_test_data.py
"""

import pandas as pd
import datetime

now = datetime.datetime.now()


def t(**kwargs):
    """Shorthand: t(minutes=10) -> now + 10 minutes. Negative values go into the past."""
    return now + datetime.timedelta(**kwargs)


def med(med_id, name, ingredients, freq, next_time, on_hand, per_dose=1,
        urgency="Medium", category="OTC", expiry="2027-03-15",
        instructions="Take with food", days=10, rating=3):
    """Builds one row with the full column set so every test case stays short."""
    return {
        "med_id": med_id, "medication_name": name, "active_ingredients": ingredients,
        "dosage_frequency_in_hours": freq, "Usage_and_Safety_Instructions": instructions,
        "Urgency": urgency, "category": category, "quantity_on_hand": on_hand,
        "expiration_date": expiry, "compliance_rating": rating, "pills_per_dose": per_dose,
        "days": days, "next_intake_time": next_time, "quantity_needed": days,
        "start_date": t(days=-5), "end_date": t(days=days - 5),
    }


rows = [
    # --- SCHEDULE: due soon or inside the 30-min grace window ---
    med(1, "Tylenol", "Acetaminophen", 6, t(minutes=5), 20, rating=4),
    med(2, "Ibuprofen", "Ibuprofen", 8, t(minutes=-10), 15, expiry="2026-09-25", rating=2),
    med(3, "Vitamin D", "Cholecalciferol", 24, t(minutes=-29), 30, category="Supplement"),  # edge: just inside grace

    # --- SCHEDULE: later today, within 24h ---
    med(4, "NyQuil", "Acetaminophen, Dextromethorphan", 8, t(hours=3), 8, per_dose=2,
        instructions="Avoid alcohol", expiry="2026-10-05"),
    med(5, "Amoxicillin", "Amoxicillin", 8, t(hours=6), 6, urgency="High",
        category="Prescription", instructions="Complete full course", expiry="2026-11-20", rating=4),
    med(6, "Loratadine", "Loratadine", 24, t(hours=23), 12),           # edge: just inside 24h
    med(7, "Multivitamin", "Mixed vitamins", 12, t(hours=2), 2, per_dose=2,
        category="Supplement"),                                        # stock exactly equals dose

    # --- MISSED: more than 30 min overdue ---
    med(8, "Cetirizine", "Cetirizine", 24, t(minutes=-31), 10),        # edge: just past grace
    med(9, "Lisinopril", "Lisinopril", 24, t(hours=-5), 10, urgency="High",
        category="Prescription", instructions="Take same time daily",
        expiry="2027-06-01", days=30, rating=5),
    med(10, "Omeprazole", "Omeprazole", 24, t(hours=-2), 0,
        category="Prescription", instructions="Take before breakfast"),  # missed AND out of stock

    # --- NEITHER: outside the 24h window ---
    med(11, "Zinc", "Zinc sulfate", 24, t(hours=26), 40, category="Supplement"),  # beyond 24h

    # --- NEITHER: not enough on hand (hidden from schedule, not overdue) ---
    med(12, "Aspirin", "Aspirin", 6, t(minutes=2), 0, days=15, rating=3),         # 0 on hand
    med(13, "Codeine Syrup", "Codeine", 8, t(hours=1), 1, per_dose=2,
        category="Prescription"),                                                 # 1 on hand, needs 2

    # --- As-needed / no fixed schedule (frequency = 0) ---
    med(14, "Band-Aid Antiseptic", "Benzalkonium Chloride", 0, t(hours=1), 25,
        urgency="Low", category="First Aid", instructions="Apply to clean wound as needed",
        expiry="2027-08-10", days=1, rating=5),

    # --- Already expired ---
    med(15, "Old Cough Syrup", "Dextromethorphan", 8, t(hours=2), 4,
        urgency="Low", instructions="Take every 8 hours as needed",
        expiry="2025-05-01", days=5),

    # --- Duplicate name, different id (tests med_id-based lookups) ---
    med(16, "Tylenol", "Acetaminophen", 6, t(hours=8), 20, rating=4),
]

df = pd.DataFrame(rows)
df.to_csv("meds.csv", index=False)

intake_rows = [
    {"med_id": 1, "intake_time": t(days=-1)},
    {"med_id": 9, "intake_time": t(days=-2)},
]
pd.DataFrame(intake_rows).to_csv("intake_log.csv", index=False)

print("Done. Generated relative to:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("- Schedule (expect 1,2,3,4,5,6,7,16): due now, inside grace, or within 24h with stock")
print("- Missed (expect 8,9,10): more than 30 min overdue (10 is also out of stock)")
print("- Neither: 11 (beyond 24h), 12 and 13 (not enough stock), 14 (as-needed), 15 (expired)")
print("Note: 14 and 15 only stay out if your code filters on frequency 0 / expiry - otherwise they show up in the schedule.")