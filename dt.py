"""
Generates fresh meds.csv and intake_log.csv for testing, with all timestamps
computed relative to the moment this script is run - so nothing goes "stale"
no matter when you actually test.

Run this right before opening the Streamlit app:
    python generate_test_data.py
"""

import pandas as pd
import datetime

now = datetime.datetime.now()


def t(**kwargs):
    """Shorthand: t(minutes=10) -> now + 10 minutes. Negative values go into the past."""
    return now + datetime.timedelta(**kwargs)


rows = [
    # --- Ready to log RIGHT NOW (within the 30-min grace window) ---
    {"med_id": 1, "medication_name": "Tylenol", "active_ingredients": "Acetaminophen",
     "dosage_frequency_in_hours": 6, "Usage_and_Safety_Instructions": "Take with food",
     "Urgency": "Medium", "category": "OTC", "quantity_on_hand": 20,
     "expiration_date": "2027-03-15", "compliance_rating": 4, "pills_per_dose": 1, "days": 10,
     "next_intake_time": t(minutes=5), "quantity_needed": 10,
     "start_date": t(days=-5), "end_date": t(days=5)},

    {"med_id": 2, "medication_name": "Ibuprofen", "active_ingredients": "Ibuprofen",
     "dosage_frequency_in_hours": 8, "Usage_and_Safety_Instructions": "Take with food",
     "Urgency": "Medium", "category": "OTC", "quantity_on_hand": 15,
     "expiration_date": "2026-09-25", "compliance_rating": 2, "pills_per_dose": 1, "days": 7,
     "next_intake_time": t(minutes=-10), "quantity_needed": 7,   # already due, still within grace
     "start_date": t(days=-3), "end_date": t(days=4)},

    # --- Too early to log (outside the grace window) ---
    {"med_id": 3, "medication_name": "NyQuil", "active_ingredients": "Acetaminophen, Dextromethorphan",
     "dosage_frequency_in_hours": 8, "Usage_and_Safety_Instructions": "Avoid alcohol",
     "Urgency": "Medium", "category": "OTC", "quantity_on_hand": 8,
     "expiration_date": "2026-10-05", "compliance_rating": 3, "pills_per_dose": 2, "days": 5,
     "next_intake_time": t(hours=3), "quantity_needed": 10,
     "start_date": t(days=-2), "end_date": t(days=3)},

    {"med_id": 4, "medication_name": "Amoxicillin", "active_ingredients": "Amoxicillin",
     "dosage_frequency_in_hours": 8, "Usage_and_Safety_Instructions": "Complete full course",
     "Urgency": "High", "category": "Prescription", "quantity_on_hand": 6,
     "expiration_date": "2026-11-20", "compliance_rating": 4, "pills_per_dose": 1, "days": 10,
     "next_intake_time": t(hours=6), "quantity_needed": 10,
     "start_date": t(days=-3), "end_date": t(days=7)},

    # --- Overdue / missed (already past due, won't show on the schedule) ---
    {"med_id": 5, "medication_name": "Lisinopril", "active_ingredients": "Lisinopril",
     "dosage_frequency_in_hours": 24, "Usage_and_Safety_Instructions": "Take same time daily",
     "Urgency": "High", "category": "Prescription", "quantity_on_hand": 10,
     "expiration_date": "2027-06-01", "compliance_rating": 5, "pills_per_dose": 1, "days": 30,
     "next_intake_time": t(hours=-5), "quantity_needed": 30,
     "start_date": t(days=-30), "end_date": t(hours=-5)},

    # --- Zero on hand (should fail with "not enough on hand", not "too early") ---
    {"med_id": 6, "medication_name": "Aspirin", "active_ingredients": "Aspirin",
     "dosage_frequency_in_hours": 6, "Usage_and_Safety_Instructions": "Take with food",
     "Urgency": "Medium", "category": "OTC", "quantity_on_hand": 0,
     "expiration_date": "2026-10-10", "compliance_rating": 3, "pills_per_dose": 1, "days": 15,
     "next_intake_time": t(minutes=2), "quantity_needed": 15,
     "start_date": t(days=-5), "end_date": t(days=10)},

    # --- As-needed / no fixed schedule (frequency = 0) ---
    {"med_id": 7, "medication_name": "Band-Aid Antiseptic", "active_ingredients": "Benzalkonium Chloride",
     "dosage_frequency_in_hours": 0, "Usage_and_Safety_Instructions": "Apply to clean wound as needed",
     "Urgency": "Low", "category": "First Aid", "quantity_on_hand": 25,
     "expiration_date": "2027-08-10", "compliance_rating": 5, "pills_per_dose": 1, "days": 1,
     "next_intake_time": t(hours=1), "quantity_needed": 1,
     "start_date": now, "end_date": t(days=1)},

    # --- Already expired ---
    {"med_id": 8, "medication_name": "Old Cough Syrup", "active_ingredients": "Dextromethorphan",
     "dosage_frequency_in_hours": 8, "Usage_and_Safety_Instructions": "Take every 8 hours as needed",
     "Urgency": "Low", "category": "OTC", "quantity_on_hand": 4,
     "expiration_date": "2025-05-01", "compliance_rating": 3, "pills_per_dose": 1, "days": 5,
     "next_intake_time": t(hours=2), "quantity_needed": 5,
     "start_date": t(days=-500), "end_date": t(days=-495)},
]

df = pd.DataFrame(rows)
df.to_csv("meds.csv", index=False)

intake_rows = [
    {"med_id": 1, "intake_time": t(days=-1)},
    {"med_id": 5, "intake_time": t(days=-2)},
]
pd.DataFrame(intake_rows).to_csv("intake_log.csv", index=False)

print("Done. Generated relative to:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("- Tylenol (1) and Ibuprofen (2): loggable now")
print("- NyQuil (3) and Amoxicillin (4): too early")
print("- Lisinopril (5): overdue, off the 24h schedule")
print("- Aspirin (6): loggable-timing but 0 on hand")
print("- Band-Aid (7): as-needed, frequency 0")
print("- Old Cough Syrup (8): expired")