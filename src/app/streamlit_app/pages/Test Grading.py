
import streamlit as st

st.title('Grade Questions')

# Inputs for test number, question number, and grade
test_number = st.number_input('Test Number', min_value=1, value=1, step=1, key='grade_test_number')
question_number = st.number_input('Question Number', min_value=1, value=1, step=1, key='grade_question_number')
grade = st.select_slider('Grade', options=['Bad', 'Poor', 'Good', 'Excellent'])

# Button to save the grade in session state
if st.button('Save Grade'):
    if 'grades' not in st.session_state:
        st.session_state.grades = {}
    
    st.session_state.grades[(test_number, question_number)] = grade
    st.success(f'Grade for Question {question_number} in Test {test_number} saved as {grade}.')