import streamlit as st
from app.data.competencies import get_compentencies_for_subject_code, get_all_subjects


def main():
    # st.title("Test Category Input")

    # question = st.text_input("Enter a question")

    # categories = get_compentencies_for_subject_code("MA")["bezeichnung"].unique()
    # dropdown = st.selectbox("Select a test category",
    #                         [descr for descr in categories])

    # # Display the test categories
    # if dropdown != ' ':

    #     st.write("Test Categories:")
    #     st.write(question, dropdown)

    

    st.title('Add Question Category')

    # Inputs for test number, question number, and category
    test_number = st.number_input('Test Number', min_value=1, value=1, step=1)
    question_number = st.number_input('Question Number', min_value=1, value=1, step=1)
    question = st.text_input("Enter the question numbers")
    subjects = get_all_subjects()
    subject = st.selectbox("Select a subject", subjects)
    categories = get_compentencies_for_subject_code(subject)["bezeichnung"]
    categories_shortened = list(categories.str.replace("Die Schülerinnen und Schüler ", ""))

    category = st.selectbox("Select a test category  \n"
                            "Die Schülerinnen und Schüler ", categories_shortened)

    # Button to save the category in session state
    if st.button('Save Category'):
        if 'question_categories' not in st.session_state:
            st.session_state.question_categories = {}

        st.session_state.question_categories[(test_number, question_number)] = category
        st.success(
            f'Question {question_number} for Test {test_number} added.'
        )


if __name__ == "__main__":
    main()
