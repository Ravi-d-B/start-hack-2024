# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt
from app.streamlit_app.database import get_student_tests
from app.streamlit_app.database import (
    get_students, get_student_tests,
    get_student_test_evaluations, get_all_student_test_evaluations
)
from app.data.competencies import get_all_subjects, get_compentencies_for_subject_code

from app.streamlit_app.database import (
    get_students, get_student_tests,
    get_student_test_evaluations, get_all_student_test_evaluations
)


# st.title('Student Category Scores Over Tests')

def plot_results(df):
    fig = plt.figure(figsize=(10, 5))
    plt.plot(df['test_date'], df['score'], marker='o')
    # Map axis labels [0,1,2,3,4] -> ['','Bad','Poor','Good','Excellent']
    plt.yticks([0, 1, 2, 3, 4, 5], ['',
                                    'Das Klappt noch nicht',
                                    'Das Gelingt mit teilweise',
                                    'Das kann ich gut',
                                    'Das kann ich sehr gut',
                                    ''])
    st.pyplot(fig)


students = get_students()

# Dropdown of students
student = st.selectbox('Select a student',
                       students,
                       format_func=lambda student: student.name)
subjects = get_all_subjects()
if 'subject' not in st.session_state:
    st.session_state.subject = subjects[0]
st.session_state.subject = st.selectbox("Select a subject", subjects,
                                        index=subjects.index(st.session_state.subject))

student = students[0]

evals = student.get_student_graph_data()

# Filter on subject
evals = evals.query('code.str.contains(@st.session_state.subject)')
# average scores for the same code on the same date
evals = evals.groupby(['test_date', 'code'])["score"].mean().reset_index()

plot_results(evals)
