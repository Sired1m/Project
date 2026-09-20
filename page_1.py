import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module


meds = module.load_meds()
today_meds = module.schedule_builder(meds)
today_meds["display_label"] = today_meds["medication_name"] + " — " + today_meds["next_intake_time"].astype(str)
if today_meds.empty:
    st.info("Nothing scheduled in the next 24 hours.")
else:
    op = st.selectbox("today's Meds",today_meds["display_label"])
    med_id = today_meds.loc[today_meds["display_label"] == op, "med_id"].iloc[0]
    if st.button("Log intake"):
        result = module.create_intake_record(meds, med_id)
    st.table(today_meds, border="horizontal")