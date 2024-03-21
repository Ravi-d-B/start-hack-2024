import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
)

first_names = ["John", "Emily", "Michael"]
last_names = ["Smith", "Johnson", "Williams"]

st.title("Test Grading")

# Define your list of options
options = ['Test 1', 'Test 2']

all_questions = [["Is it okay?", "Is it good?"],["Why", "Where", "When"]]

test_questions = {test: questions for test, questions in zip(options, all_questions)}

# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    test_questions.keys())

# Create a list of dictionaries, with each dictionary representing a row
data = []
for i, (first, last) in enumerate(zip(first_names, last_names)):
    data.clear()
    st.subheader(f"{first} {last}")
    for (question) in zip(test_questions[option]):
        row = {
            "Question": question,
            "Das Klappt noch nicht": False,
            "Das Gelingt mit teilweise": False,
            "Das kann ich gut": False,
            "Das kann ich sehr gut": False}
        data.append(row)
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, use_container_width=True, disabled="col1", hide_index="true", height=None, key=i)
