import pandas as pd
import numpy as np
import datetime
import streamlit as st

def addNewRecord(data_frame, new_record):
    df = pd.concat([data_frame,new_record], ignore_index=True)
    return df

#st.daialoge for adding a medicen
#
#columns that will be added:
#category
#pill_per_day
#number_of _days
#rating 1-5

#calculate medication quantities

def createRecord(medication_name, active_ingredients, dosage_frequency_in_hours,Usage_and_Safety_Instructions,Urgency,category,quantity_on_hand,expiration_date,compliance_rating,pills_per_dose, days):
    try:
        rdf = pd.DataFrame({"medication_name":[medication_name], "active_ingredients":[list_to_string(active_ingredients)], "dosage_frequency_in_hours":[dosage_frequency_in_hours], "Usage_and_Safety_Instructions":[Usage_and_Safety_Instructions], "Urgency":[Urgency], "category":[category], "quantity_on_hand":[quantity_on_hand], "expiration_date":[expiration_date],"compliance_rating":[compliance_rating], "pills_per_dose":[pills_per_dose], "days":days })
    except TypeError as e:
        print(f"Caught error: {e}")
    return rdf

def list_to_string(lst, separator=', '):
    return separator.join(lst)

def search_by_ingredient(data_frame,ingredient):
    df = data_frame[data_frame.active_ingredients.str.contains(ingredient,case=False)]
    if check_overdose(df):
        st.warning(f"You might have a risk of overdose", icon="⚠️")

    return df

def check_overdose(data_frame):
    if len(data_frame) >= 3:
        return True
    return False

def str_to_list


