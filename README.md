# Meds Tracker
 
A Streamlit app for tracking medications, logging doses, checking refills, and getting AI-assisted drug interaction summaries.
 
## Pages
 
- **Log Intake** – shows meds due in the next 24 hours and any missed doses, with a button to log them.
- **View All Medications** – full medication list, filterable by category, plus expired / expiring-soon views.
- **Add Medication** – form to add a new medication. Can auto-fetch active ingredients from RxNav by name.
- **Search by Ingredient** – search meds by active ingredient, flags possible duplicate/overdose risk.
- **Refill Request List** – shows meds running low and lets you add them to a refill request list.
- **Interaction & Safety Advisor** – sends your current active medications to an AI model (via OpenRouter) to summarize possible drug interactions and explain medical terms in plain language.
