import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module


meds = module.load_meds()
today_meds = module.schedule_builder(meds)
if "just_logged" not in st.session_state:
    st.session_state["just_logged"] = False
today_meds["display_label"] = today_meds["medication_name"] + " — " + today_meds["next_intake_time"].astype(str)
if today_meds.empty:
    st.info("Nothing scheduled in the next 24 hours.")
else:
    op = st.selectbox("today's Meds",today_meds["display_label"])
    med_id = today_meds.loc[today_meds["display_label"] == op, "med_id"].iloc[0]
    if st.button("Log intake", disabled=st.session_state["just_logged"]):
        result, message = module.create_intake_record(meds, med_id)
        if result is not None:
            intake_log = module.load_intake_log()
            module.add_new_intake_record(intake_log, result)
            st.session_state["just_logged"] = True
            st.rerun()
        else:
            st.error(message)

    if st.session_state["just_logged"]:
        next_time = meds.loc[meds["med_id"] == med_id, "next_intake_time"].iloc[0]
        st.success(f"Logged. Next dose due at {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.session_state["just_logged"] = False

    display_df = today_meds[["medication_name", "next_intake_time"]].copy()
    display_df["next_intake_time"] = display_df["next_intake_time"].dt.strftime("%I:%M %p")
    st.table(display_df)