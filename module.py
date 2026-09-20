import pandas as pd
import numpy as np
import datetime
import streamlit as st

def add_new_meds_record(data_frame, new_record):
    df = pd.concat([data_frame,new_record], ignore_index=True)
    save_meds(df)
    return True

#st.daialoge for adding a medicen
#
#columns that will be added:
#category
#pill_per_day
#number_of _days
#rating 1-5

#calculate medication quantities

def create_meds_record(dataframe,medication_name, active_ingredients, dosage_frequency_in_hours,Usage_and_Safety_Instructions,Urgency,category,quantity_on_hand,expiration_date,pills_per_dose, days, compliance_rating=0, start_date=None):
     if start_date is None:
        start_date = datetime.datetime.now()
     rdf = pd.DataFrame({"med_id":[generate_id(dataframe)],
                        "medication_name":[medication_name],
                        "active_ingredients":[list_to_string(active_ingredients)],
                        "dosage_frequency_in_hours":[dosage_frequency_in_hours],
                        "Usage_and_Safety_Instructions":[Usage_and_Safety_Instructions],
                        "Urgency":[Urgency], "category":[category], "quantity_on_hand":[quantity_on_hand],
                        "expiration_date":[expiration_date],
                        "compliance_rating":[compliance_rating],
                        "pills_per_dose":[pills_per_dose],
                        "days":[days],
                        "next_intake_time": [set_new_intake_time(dosage_frequency_in_hours)],
                        "quantity_needed": [calculate_quantity_needed(pills_per_dose,days)],
                        "start_date":[start_date],
                        "end_date":[calculate_end_date(start_date,days)]})
     return rdf

def list_to_string(lst, separator=', '):
    return separator.join(lst)

def search_by_ingredient(data_frame,ingredient):
    df = data_frame[data_frame.active_ingredients.str.contains(ingredient,case=False)]
    if check_overdose(df):
        st.warning(f"You might have a risk of overdose", icon="⚠️")

    return df

def check_overdose(data_frame):
    if len(data_frame) >= 2:
        return True
    return False

def generate_id(dataframe):
    if dataframe.empty:
        return 1
    return dataframe["med_id"].max() + 1

def save_meds(dataframe):
    dataframe.to_csv("meds.csv", index=False)

def save_intake(dataframe):
    dataframe.to_csv("intake_log.csv", index=False)

def set_new_intake_time(dosage_frequency_in_hours):
    return datetime.datetime.now() + datetime.timedelta(hours=dosage_frequency_in_hours)

def load_meds():
    df = pd.read_csv("meds.csv")
    df["next_intake_time"] = pd.to_datetime(df["next_intake_time"])
    return df

def load_intake_log():
    df=pd.read_csv("intake_log.csv")
    df["intake_time"] = pd.to_datetime(df["intake_time"])
    return df

def calculate_quantity_needed(ppd, d):
    return ppd * d

def create_intake_record(medsdf, med_id):
    mask = medsdf["med_id"] == med_id
    if mask.sum() == 0:
        return None 

    current_qty = medsdf.loc[mask, "quantity_on_hand"].iloc[0]
    dose_size = medsdf.loc[mask, "pills_per_dose"].iloc[0]

    if current_qty < dose_size:
        return None
    
    rdf = pd.DataFrame({"med_id":[med_id], "intake_time":[datetime.datetime.now()]})
    dosage_frequency = medsdf.loc[mask, "dosage_frequency_in_hours"].iloc[0]
    medsdf.loc[mask, "quantity_on_hand"] = current_qty - dose_size
    medsdf.loc[mask, "next_intake_time"] = set_new_intake_time(dosage_frequency)
    save_meds(medsdf)
    return rdf

def add_new_intake_record(dataframe,new_record):
    df = pd.concat([dataframe,new_record], ignore_index=True)
    save_intake(df)
    return True

def calculate_end_date(start, nday):
    return start + datetime.timedelta(days=nday)

def schedule_builder(dataframe):
    now =  datetime.datetime.now()
    the_24h = now + datetime.timedelta(hours=24)
    return dataframe[(dataframe["next_intake_time"] >= now) & (dataframe["next_intake_time"] <= the_24h) ].sort_values(by='next_intake_time', ignore_index=True)

def list_not_taken_meds(dataframe):
    return dataframe[dataframe["next_intake_time"] < datetime.datetime.now()].sort_values(by='next_intake_time', ignore_index=True)

def load_health_tips():
    return pd.read_csv("health_tips.csv")

def get_random_tip(dataframe):
    return dataframe.sample().iloc[0]["Tips"]

def set_compliance_rating(dataframe,id, rate):
    mask = dataframe["med_id"] == id
    dataframe.loc[mask , "compliance_rating"] = rate
    save_meds(dataframe)
    return True

def sort_by_compliance_rating(dataframe):
    return dataframe.sort_values(by='compliance_rating', ignore_index=True)
