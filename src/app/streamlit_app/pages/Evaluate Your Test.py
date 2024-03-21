import streamlit as st
import pandas as pd
from streamlit_modal import Modal

from app.streamlit_app.database import *

st.set_page_config(
    layout="wide",
)

st.title("Test Grading")


class Test:
    def __init__(self, id, name, evaluations):
        self.id = id
        self.name = name
        self.evaluations = evaluations

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_evaluations(self):
        return self.evaluations


tests = get_tests()

Tests = []

for test_row in tests:
    test_competencies = []
    for c in get_test_competencies(test_row.id):
        test_competencies.append(c.get_competency_type().type)
    Tests.append(Test(test_row.id, test_row.test_name, test_competencies))

test_evaluations = {test.get_name(): test.get_evaluations() for test in Tests}


# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    test_evaluations.keys())

current_test = tests[0].id

for test in Tests:
    if test.get_name() == option:
        current_test = test.id


students = get_test_students(current_test)

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





def find_mark(row):
    if row[2]:
        return 1
    if row[3]:
        return 2
    if row[4]:
        return 3
    if row[5]:
        return 4

for data in student_marks:
    for idx, row in enumerate(data.itertuples(), start=1):
        st.markdown(f"{find_mark(row)}")




# Modal Stuff
# def saveData():
#     print(get_test_competencies(4)[0].get_competency_type().type)
#     modal.close()
#
#
# modal = Modal(
#     "Do you want to confirm changes?",
#     key="confirm modal",
# )
#
# st.button("Save Changes", on_click=modal.open, type="primary")
#
#
# if modal.is_open():
#     with modal.container():
#         col1, col2, col3 = st.columns([6, 1, 1])
#         with col2:
#             st.button('Confirm')
#         with col3:
#             st.button('Cancel', on_click=saveData)
