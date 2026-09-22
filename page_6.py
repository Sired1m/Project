import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

df = module.load_meds()
active_meds = module.exclude_expired_list(df)

st.title("Interaction & Safety Advisor")

st.dataframe(active_meds[["medication_name", "active_ingredients", "category"]])

if st.button("Check interactions"):
    if active_meds.empty:
        st.info("No active medications to check.")
    else:
        prompt = module.build_prompt(active_meds)
        summary = module.ask_ai(prompt)
        st.write(summary)