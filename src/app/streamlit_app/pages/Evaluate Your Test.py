import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
)


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


students = [Student("John", "Smith"), Student("Emily", "Johnson"), Student("Michael", "Williams")]


st.title("Test Grading")

# Define your list of options
options = ['Test 1', 'Test 2']

all_questions = [["Is it okay?", "Is it good?"], ["Why", "Where", "When"]]

test_questions = {test: questions for test, questions in zip(options, all_questions)}

# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    test_questions.keys())

# Create a list of dictionaries, with each dictionary representing a row
data = []
for i, student in enumerate(students):
    data.clear()
    st.subheader(f"{student.first_name} {student.last_name}")
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
