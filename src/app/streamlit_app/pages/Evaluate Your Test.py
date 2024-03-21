import streamlit as st
import pandas as pd
from app.streamlit_app.database import setup_database, get_students, add_to_students, add_to_evaluation_types, get_evaluation_types, add_to_tests, get_tests, add_test_evaluation_to_test, get_test_evaluations, get_all_test_evaluations, add_student_to_tests, add_test_evaluation_to_student, get_student_tests, get_student_test_evaluations, get_all_student_test_evaluations, get_test_students, seed_database

print(get_students())

st.set_page_config(
    layout="wide",
)

st.title("Test Grading")


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Test:
    def __init__(self, name, evaluations):
        self.name = name
        self.evaluations = evaluations

    def get_name(self):
        return self.name

    def get_evaluations(self):
        return self.evaluations


students = [Student("John", "Smith"), Student("Emily", "Johnson"),
            Student("Michael", "Williams")]

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
    st.subheader(f"{student.first_name} {student.last_name}")
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
        st.markdown(f"{row[1][0]}")
        if(row[2]):
            st.markdown(row[2])


def find_mark(row):
    if row[2]:
        return 1
    if row[3]:
        return 2
    if row[4]:
        return 3
    if row[5]:
        return 4

