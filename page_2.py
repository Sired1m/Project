import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

df = module.load_meds()

st.title("All Your Meds")

category = st.radio(
    "Filter by",
    ["All", "Prescription", "OTC", "Supplement", "First Aid"], horizontal=True
)

if category == "All":
    st.dataframe(df)
else:
    st.dataframe(df[df["category"] == category])

st.title("expired meds")

expired_df = module.list_expiered_list(df)

st.dataframe(expired_df)

st.title("expired soon meds")

expired_soon_df = module.create_expiered_soon_meds_list(df)

st.dataframe(expired_soon_df)