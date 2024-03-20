import streamlit as st

def main():
    st.title("Test Category Input")

    question = st.text_input("Enter a question")
    dropdown = st.selectbox("Select a test category", [' ','addition', 'subtraction', 'multiplication'])

    # Display the test categories
    if dropdown != ' ':

        st.write("Test Categories:")
        st.write(question, dropdown)

    
        

if __name__ == "__main__":
    main()