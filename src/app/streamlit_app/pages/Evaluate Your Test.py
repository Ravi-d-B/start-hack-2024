import streamlit as st
import pandas as pd
from streamlit_modal import Modal

from app.streamlit_app.database import setup_database, get_students, add_to_students, add_to_evaluation_types, get_evaluation_types, add_to_tests, get_tests, add_test_evaluation_to_test, get_test_evaluations, get_all_test_evaluations, add_student_to_tests, add_test_evaluation_to_student, get_student_tests, get_student_test_evaluations, get_all_student_test_evaluations, get_test_students, seed_database

st.set_page_config(
    layout="wide",
)

st.title("Test Grading")


class Test:
    def __init__(self, name, evaluations):
        self.name = name
        self.evaluations = evaluations

    def get_name(self):
        return self.name

    def get_evaluations(self):
        return self.evaluations


def find_mark(row):
    if row[2]:
        return 1
    if row[3]:
        return 2
    if row[4]:
        return 3
    if row[5]:
        return 4

students = get_students()

Test1 = Test("Test1", ["können Bilder wahrnehmen, beobachten und darüber reflektieren", "können Bilder wahrnehmen, beobachten und darüber reflektieren."])
Test2 = Test("Test2", ["Why", "Where", "When"])

Tests = [Test1, Test2]

test_evaluations = {test.get_name(): test.get_evaluations() for test in Tests}

# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    test_evaluations.keys())

# Create Student Marks Array
student_marks = []

# Create a list of dictionaries, with each dictionary representing a row
data = []
for i, student in enumerate(students):
    data.clear()
    st.subheader(f"{student.name}")
    for (question) in zip(test_evaluations[option]):
        row = {
            "Evaluations": question,
            "Das Klappt noch nicht": False,
            "Das Gelingt mit teilweise": False,
            "Das kann ich gut": False,
            "Das kann ich sehr gut": False}
        data.append(row)
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, use_container_width=True, disabled="col1", hide_index="true", height=None, key=i)
    student_marks.append(edited_df)

# print(edited_df.keys())

for data in student_marks:
    for idx, row in enumerate(data.itertuples(), start=1):
        st.markdown(f"{find_mark(row)}")


def saveData():
    print(students[1].id)
    modal.close()


st.button("Save Changes", on_click=saveData, type="primary")

modal = Modal(
    "Do you want to confirm changes?",
    key="confirm modal",
)

open_modal = st.button("Open", on_click=modal.open)


if modal.is_open():
    with modal.container():
        col1, col2, col3 = st.columns([6, 1, 1])
        with col2:
            st.button('Confirm')
        with col3:
            st.button('Cancel', on_click=saveData)
