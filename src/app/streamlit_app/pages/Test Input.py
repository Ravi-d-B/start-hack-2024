import streamlit as st
from app.data.competencies import get_compentencies_for_subject_code, get_all_subjects


def main():
    st.title("Test Input Form")

    question = st.text_input("Enter the question numbers")
    subjects = get_all_subjects()
    subject = st.selectbox("Select a subject", subjects)
    categories = get_compentencies_for_subject_code(subject)["bezeichnung"].unique()
    dropdown = st.selectbox("Select a test category", list(categories))

    # Display the test categories
    if dropdown != ' ':

        st.write("Test Categories:")
        st.write(question, dropdown)


if __name__ == "__main__":
    main()
