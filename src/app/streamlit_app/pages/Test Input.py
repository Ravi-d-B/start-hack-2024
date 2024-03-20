import streamlit as st
from app.data.competencies import get_compentencies_for_subject_code

def main():
    st.title("Test Category Input")

    question = st.text_input("Enter a question")

    categories = get_compentencies_for_subject_code("MA")["bezeichnung"].unique()
    dropdown = st.selectbox("Select a test category",
                            [descr for descr in categories])

    # Display the test categories
    if dropdown != ' ':

        st.write("Test Categories:")
        st.write(question, dropdown)

    
        

if __name__ == "__main__":
    main()