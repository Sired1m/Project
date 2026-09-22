import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module
import datetime
st.title("Add med")
'''
med_id,
medication_name,
active_ingredients,
dosage_frequency_in_hours,
Usage_and_Safety_Instructions,
Urgency,
category,
quantity_on_hand,
expiration_date,
compliance_rating,
pills_per_dose,
days,
next_intake_time,
quantity_needed,
start_date,
end_date
'''

med_name = st.text_input("med name")
active_ingredients = []

if "fetched_ingredients" not in st.session_state:
    st.session_state["fetched_ingredients"] = []

if st.button("Add ingrediants"):
    active_ingredients = module.fetch_med_ingrediants(med_name)
    st.session_state["fetched_ingredients"] = active_ingredients

options = st.multiselect("ingrediants", st.session_state["fetched_ingredients"],accept_new_options=True)

dosage_frequency_in_hours = st.number_input(
    "Insert the dosage frequency in hours", value=1, placeholder="Type a number...", min_value=1, max_value=24,step=1)

Usage_and_Safety_Instructions = st.text_input("Usage and Safety Instructions")

category = st.selectbox("What category?",["Prescription", "OTC", "Supplement", "First Aid"])

urgency = st.selectbox("What the urgency?",["High", "Mid", "Low"])

quantity_on_hand = st.number_input(
    "Insert the quantity on hand", value=1, placeholder="Type a number...", min_value=1,step=1)

expiration_date= st.date_input("When's the med expiration date", datetime.date.today(), min_value="today")

pills_per_dose = st.number_input(
    "Insert the number of pills per dose", value=1, placeholder="Type a number...", min_value=1,max_value=20,step=1)

days = st.number_input(
    "Insert the number of days you plan to take the med", value=1, placeholder="Type a number...", min_value=1,step=1)