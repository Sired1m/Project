import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

df=module.load_meds()

st.title("Add Medication")

if "add_success" in st.session_state:
    st.success(st.session_state.pop("add_success"))

med_name = st.text_input("med name")
active_ingredients = []

if "fetched_ingredients" not in st.session_state:
    st.session_state["fetched_ingredients"] = []

if st.button("Add ingrediants"):
    active_ingredients = module.fetch_med_ingrediants(med_name)
    if not active_ingredients:
        st.error("Could not find the ingredients for this medication.")
        st.session_state["fetched_ingredients"] = []
    else:
        st.session_state["fetched_ingredients"] = active_ingredients
        st.success("Ingredients found!")

with st.form("add_med_form", clear_on_submit=True):

    options = st.multiselect(
        "Ingredients",
        st.session_state["fetched_ingredients"],
        accept_new_options=True
    )

    dosage_frequency_in_hours = st.number_input(
        "Dosage frequency in hours",
        min_value=1,
        max_value=24,
        value=1,
        step=1
    )

    Usage_and_Safety_Instructions = st.text_input(
        "Usage and Safety Instructions"
    )

    category = st.selectbox(
        "Category",
        ["Prescription", "OTC", "Supplement", "First Aid"]
    )

    urgency = st.selectbox(
        "Urgency",
        ["High", "Mid", "Low"]
    )

    quantity_on_hand = st.number_input(
        "Quantity on hand",
        min_value=1,
        value=1,
        step=1
    )

    expiration_date = st.date_input(
        "Expiration date",
        datetime.date.today(),
        min_value=datetime.date.today()
    )

    pills_per_dose = st.number_input(
        "Number of pills per dose",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

    days = st.number_input(
        "Number of days you plan to take the medication",
        min_value=1,
        value=1,
        step=1
    )

    submitted = st.form_submit_button("Add Medication")

    if submitted:
        if not med_name.strip():
            st.error("Please enter a medication name.")

        elif not options:
            st.error("Please select at least one ingredient.")

        else:
            rdf = module.create_meds_record(df, med_name, options, dosage_frequency_in_hours, Usage_and_Safety_Instructions, urgency, category, quantity_on_hand, expiration_date, pills_per_dose, days)
            module.add_new_meds_record(df, rdf)
            st.success(f"{med_name} added successfully!")
            st.session_state["fetched_ingredients"] = []