import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

pages = [
    st.Page("page_1.py", title="Log Intake"),
    st.Page("page_2.py", title="View All Medications"),
    st.Page("page_3.py", title="Add Medication"),
    st.Page("page_4.py", title="Search by Ingredient"),
    st.Page("page_5.py", title="Refill Request List"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()