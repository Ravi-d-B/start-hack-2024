import streamlit as st

from app.data.competencies import get_all_subjects, get_compentencies_for_subject_code
from app.streamlit_app.database import (add_to_tests, add_test_competency_to_test,
                                        get_test_by_name, get_all_test_competency_types,
                                        get_competency_type_by_name)

def add_row():
    st.session_state.table_data.append({
        'question_nums': [],  # Ensure this list is empty when adding a new row
        'competency': categories_shortened[0],
    })


def delete_row(index: int):
    st.session_state.table_data.pop(index)


def save_test():
    # Iterate over each row in the table_data
    for competency in st.session_state.table_data:
        question_numbers = competency['question_nums']
        competency = competency['competency']

        # Save each competency with the associated question numbers
        if competency not in st.session_state.competencies.keys():
            st.session_state.competencies[competency] = []
        for num in question_numbers:
            if num not in st.session_state.competencies[competency]:
                st.session_state.competencies[competency].append(num)

    # Add test to DB
    add_to_tests(st.session_state.test_name)
    test_id = get_test_by_name(st.session_state.test_name).id
    for competency, question_numbers in st.session_state.competencies.items():
        comp_id = get_competency_type_by_name(competency).id
        add_test_competency_to_test(test_id, comp_id, question_numbers)


def initialize_test_table():
    if 'competencies' not in st.session_state:
        st.session_state.competencies = {}

    subjects = get_all_subjects()
    if 'subject' not in st.session_state:
        st.session_state.subject = subjects[0]
    st.session_state.subject = st.selectbox("Select a subject", subjects,
                                            index=subjects.index(st.session_state.subject))

    if 'table_data' not in st.session_state:
        st.session_state.table_data = []

    if 'num_questions' not in st.session_state:
        st.session_state.num_questions = 10

    if 'test_name' not in st.session_state:
        st.session_state.test_name = 1


if __name__ == "__main__":

    # Initialize or update the competencies in the session state based on selections
    initialize_test_table()

    st.session_state.test_name = st.text_input('Test Name',
                                                value=st.session_state.test_name,
                                                )

    categories = get_compentencies_for_subject_code(st.session_state.subject)["bezeichnung"]
    categories_shortened = list(categories.str.replace("Die Schülerinnen und Schüler ", ""))

    st.session_state.num_questions = st.number_input('Number of Questions', min_value=1,
                                                     value=st.session_state.num_questions, step=1)

    if len(st.session_state.table_data) < 1:
        add_row()  # Adds missing rows based on the current number of questions

    # Display the table with input fields
    for ind, row in enumerate(st.session_state.table_data):
        cols = st.columns([1, 2, 0.6])

        # Column for Question Number Input
        with cols[0]:
            question_options = list(range(1, st.session_state.num_questions + 1))
            selected_questions = st.multiselect('Questions', question_options,
                                                default=row['question_nums'], key=f'qn_{ind}')
            row['question_nums'] = selected_questions

        # Column for Competency Selection
        with cols[1]:
            row['competency'] = st.selectbox("Competency", categories_shortened,
                                             index=categories_shortened.index(row['competency']),
                                             key=f'comp_{ind}')

        # Column for Delete Button
        with cols[2]:
            if st.button("Delete", key=f'del_{ind}'):
                delete_row(ind)

    # Buttons to add a new row
    st.button("Add Row", on_click=add_row)

    if st.button('Save Test'):
        save_test()

        st.success(
            'Save successful.'
        )
