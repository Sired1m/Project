import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

df = module.load_meds()
ingredient = st.text_input("Enter ingredient")
if ingredient:
    searched = module.search_by_ingredient(df, ingredient)
    if searched.empty:
        st.info(f"There is no medicine that have {ingredient}")
    else:
        st.dataframe(searched)
        if len(searched) > 1:
            st.info(f"{ingredient} is repeted and might cause compounding/overdose risks")