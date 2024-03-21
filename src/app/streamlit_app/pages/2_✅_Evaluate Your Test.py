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


class StudentAnswers:
    def __init__(self, student_id, anwsers):
        self.student_id = student_id
        self.anwsers = anwsers

    def get_id(self):
        return self.student_id

    def get_anwsers(self):
        return self.anwsers


loaded_tests = get_tests()
current_test = loaded_tests[0].id

tests_display = []


for test in loaded_tests:
    test_competencies = {}
    for competency in get_test_competencies(test.id):
        competency_id = competency.id
        competency_type = competency.get_competency_type().type
        test_competencies[competency_type] = competency_id

    tests_display.append(Test(test.id, test.test_name, test_competencies.keys()))


test_evaluations = {test.get_name(): test.get_evaluations() for test in tests_display}


# Use the select box widget
option = st.selectbox(
    'Select Test for Grading',
    test_evaluations.keys())

for test in tests_display:
    if test.get_name() == option:
        current_test = test.id

current_competencies = {}

for competency in get_test_competencies(current_test):
    competency_id = competency.id
    competency_type = competency.get_competency_type().type
    current_competencies[competency_type] = competency_id


students = get_test_students(current_test)

# Create Student Marks Array
all_student_results = []

# Create a list of dictionaries, with each dictionary representing a row
data = []

for i, student in enumerate(students):
    data.clear()
    marks = get_student_test_evaluations(student.id, current_test)
    for mark in marks:
        print(mark.score)
    st.subheader(f"{student.name} - {student.id} ")

    for (question) in zip(test_evaluations[option]):
        row = {
            "Competencies": question,
            "Das Klappt noch nicht": False,
            "Das Gelingt mit teilweise": False,
            "Das kann ich gut": False,
            "Das kann ich sehr gut": False}
        data.append(row)

    df = pd.DataFrame(data)
    question_answers = st.data_editor(df, use_container_width=True, disabled="col1", hide_index="true", height=None, key=i)
    all_student_results.append(StudentAnswers(student.id, question_answers))


def get_mark(result):
    if result.iloc[1]:
        return 1
    if result.iloc[2]:
        return 2
    if result.iloc[3]:
        return 3
    if result.iloc[4]:
        return 4
    else:
        return 0

def get_competency_id(result):
    result_type = result.iloc[0][0]
    return current_competencies[result_type]

def saveData():
    for student_temp in all_student_results:
        for index in range(len(student_temp.get_anwsers())):
            question = student_temp.get_anwsers().iloc[index]
            add_test_evaluation_to_student(student_temp.get_id(), get_competency_id(question), get_mark(question), "")
    # modal.close()


if(st.button("Save")):
    saveData()

# if st.button('Confirm'):
#     saveData()

# modal = Modal(
#     "Do you want to confirm changes?",
#     key="confirm modal",
# )
#
# open_modal = st.button("Save")
# if open_modal:
#     modal.open()
#
#
# if modal.is_open():
#     with modal.container():
#         col1, col2, col3 = st.columns([6, 1, 1])
#         with col2:
#             if st.button('Confirm'):
#                 saveData()
#         with col3:
#             if st.button('Cancel'):
#                 modal.close()


