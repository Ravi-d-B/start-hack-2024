import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
)

first_names = ["John", "Emily", "Michael", "Sarah", "Jessica", "Jacob", "Mohamed", "Sophia", "Daniel", "Olivia",
               "David", "Ava", "Joseph", "Emma"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson"]

st.title("Test Grading")

# Define your list of options
options = ['Test 1', 'Test 2', 'Test 3']

test_questions = ["Is it okay?", "Is it good?"]

# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    options)

# Create a list of dictionaries, with each dictionary representing a row
data = []
for i, (first, last) in enumerate(zip(first_names, last_names)):
    data.clear()
    st.subheader(f"{first} {last}")
    for (question) in zip(test_questions):
        row = {
            "Question": question,
            "Das Klappt noch nicht": False,
            "Das Gelingt mit teilweise": False,
            "Das kann ich gut": False,
            "Das kann ich sehr gut": False}
        data.append(row)
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, use_container_width=True, disabled="col1", hide_index="true", height=None, key=i)
