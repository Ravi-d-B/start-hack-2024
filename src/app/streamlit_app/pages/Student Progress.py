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
    if df.empty:
        st.write("No data to display")
        return
    # Count number of unique cat 2
    cats = (df['cat1']+df['cat2']).unique()
    num_cats = len(cats)

    # make horizontal plots for each cat2
    fig, ax = plt.subplots(num_cats, 1, figsize=(10, 5*num_cats),
                           sharex=True)

    for i, cat_val in enumerate(cats):
        # Filter on cat2
        df_cat = df.query('(cat1 + cat2) == @cat_val')

        # Set title to code but last part dropped
        ax[i].set_title(df_cat['code'].iloc[0].rsplit('.', 1)[0])
        # Make a line for every cat3
        for cat3 in df_cat['cat3'].unique():
            df_cat3 = df_cat.query('cat3 == @cat3')
            print(df_cat3)
            ax[i].plot(df_cat3['test_date'], df_cat3['score'],
                       marker='o',
                       label=df_cat3['code'].iloc[0])
        ax[i].legend()
        ax[i].set_yticks([0, 1, 2, 3, 4, 5])
        ax[i].set_yticklabels(['',
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

evals = student.get_student_graph_data()

# Filter on subject
evals = evals.query('code.str.contains(@st.session_state.subject)')
# average scores for the same code on the same date
evals = evals.groupby(['test_date', 'code'])["score"].mean().reset_index()

# Split code into columns
evals["subjects"] = evals["code"].str.split(".").str[0]
evals["cat1"] = evals["code"].str.split(".").str[1]
evals["cat2"] = evals["code"].str.split(".").str[2]
evals["cat3"] = evals["code"].str.split(".").str[3]


plot_results(evals)
