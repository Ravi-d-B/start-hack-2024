import streamlit as st

from app.data.competencies import get_all_subjects, get_compentencies_for_subject_code


def add_row():
    st.session_state.table_data.append({
        'question_nums': [],  # Ensure this list is empty when adding a new row
        'competency': categories_shortened[0],
    })


def delete_row(index: int):
    st.session_state.table_data.pop(index)


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
        st.session_state.num_questions = 1

    if 'test_number' not in st.session_state:
        st.session_state.test_number = 1


if __name__ == "__main__":

    # Initialize or update the competencies in the session state based on selections
    initialize_test_table()

    st.session_state.test_number = st.number_input('Test Number',
                                                   min_value=1, value=st.session_state.test_number,
                                                   step=1)

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

    if st.button('Save Category'):

        # Iterate over each row in the table_data
        for row in st.session_state.table_data:
            question_numbers = row['question_nums']  # List of selected question numbers for the row
            competency = row['competency']  # The selected competency for the row

            # Save each question number with its associated competency
            for question_number in question_numbers:
                # Use a tuple of (question_number, competency) as the key
                st.session_state.competencies[question_number] = competency

        st.success(
            'Competencies for selected questions added.'
        )

    # Optional: Display the current state of question_categories for debugging
    st.write("Current question categories:", st.session_state.competencies)
