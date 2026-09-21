import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module


meds = module.load_meds()
today_meds = module.exclude_expired_list(module.schedule_builder(meds))
missed_meds = module.exclude_expired_list(module.list_not_taken_meds(meds))


def make_labels(df):
    times = df["next_intake_time"].dt.strftime("%Y-%m-%d %H:%M")
    return dict(zip(df["med_id"], df["medication_name"] + " — " + times))


def log_dose(med_id):
    result, message = module.create_intake_record(meds, med_id)
    if result is None:
        st.error(message)
        return
    intake_log = module.load_intake_log()
    module.add_new_intake_record(intake_log, result)

    row = meds.loc[meds["med_id"] == med_id].iloc[0]
    st.session_state["last_logged"] = {
        "name": row["medication_name"],
        "next_time": row["next_intake_time"].strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.rerun()


# Confirmation from the previous run, if any
if "last_logged" in st.session_state:
    info = st.session_state.pop("last_logged")
    st.success(f"Logged {info['name']}. Next dose due at {info['next_time']}")

# ---- Scheduled meds ----
if today_meds.empty:
    st.info("Nothing scheduled in the next 24 hours.")
else:
    labels = make_labels(today_meds)
    med_id = st.selectbox("Today's meds", list(labels), format_func=labels.get)
    if st.button("Log intake"):
        log_dose(med_id)

    display_df = today_meds[["medication_name", "next_intake_time"]].copy()
    display_df["next_intake_time"] = display_df["next_intake_time"].dt.strftime("%I:%M %p")
    st.table(display_df)

# ---- Missed meds ----
if not missed_meds.empty:
    missed_labels = make_labels(missed_meds)
    missed_id = st.selectbox("Missed meds", list(missed_labels), format_func=missed_labels.get)
    if st.button("Log missed meds"):
        log_dose(missed_id)

    display_mdf =  missed_meds[["medication_name","next_intake_time"]].copy()
    display_mdf["next_intake_time"] = display_mdf["next_intake_time"].dt.strftime("%I:%M %p")
    st.table(display_mdf)