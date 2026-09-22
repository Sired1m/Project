import pandas as pd
import numpy as np
import datetime
import streamlit as st
import module

meds = module.load_meds()
refill_list = module.load_refill_list()

st.title("Refill request list")

needing_refill = module.list_meds_need_refill(meds, refill_list)

if needing_refill.empty:
    st.info("Nothing is running low right now.")
else:
    st.dataframe(needing_refill[["medication_name", "quantity_on_hand", "quantity_needed"]])

    options = dict(zip(needing_refill["med_id"], needing_refill["medication_name"]))
    selected = st.multiselect("Add to refill request", list(options), format_func=options.get)

    if st.button("Add to Refill Request List"):
        to_add = needing_refill[needing_refill["med_id"].isin(selected)]
        updated = module.add_to_refill_request_list(refill_list, to_add)
        module.save_refill_list(updated)
        st.rerun()

st.title("Current refill request list")

if refill_list.empty:
    st.info("Your refill request list is empty.")
else:
    st.dataframe(refill_list[["medication_name", "active_ingredients", "quantity_on_hand", "quantity_needed"]])