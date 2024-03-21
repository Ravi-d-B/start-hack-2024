# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt
from app.streamlit_app.database import get_student_tests

from app.streamlit_app.database import (
    get_students, get_student_tests,
    get_student_test_evaluations, get_all_student_test_evaluations
)

from app.data.competencies import get_all_subjects, get_compentencies_for_subject_code, get_full_comp_df

from app.streamlit_app.graph import create_graph


st.title('Student Progression')


def plot_results(df):
    if df.empty:
        st.write("No data to display")
        return
    # Count number of unique cat 2
    cats = (df['cat1'] + df['cat2']).unique()
    num_cats = len(cats)

    # make horizontal plots for each cat2
    fig, ax = plt.subplots(num_cats, 1, figsize=(10, 5 * num_cats),
                           sharex=True)

    for i, cat_val in enumerate(cats):
        # Filter on cat2
        df_cat = df.query('(cat1 + cat2) == @cat_val')

        title_part_1 = df_cat['code'].iloc[0].rsplit('.', 2)[0:2]
        title_part_2 = df_cat['code'].iloc[0].rsplit('.', 1)[0]
        title_part_1 = get_full_comp_df().query('code == @title_part_1')['bezeichnung'].iloc[0]
        title_part_2 = get_full_comp_df().query('code == @title_part_2')['bezeichnung'].iloc[0]


        # Set title to code but last part dropped
        ax[i].set_title(f'{title_part_1} - {title_part_2}')
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

level_options = {
    "Year 1": [1] + [None] * 6,
    "Year 2": [4, 3, 2, 1, 1, 1, None],
    "Year 3": [4, 4, 4, 4, 4, 3, 3]
}

# Add a dropdown menu for selecting the level configuration
selected_option = st.selectbox(
    'Select the year for which you want to see the knowledge graph:',
    options=list(level_options.keys()),
    index=2
)

# Get the selected levels configuration
selected_levels = level_options[selected_option]

# Create the graph based on the selected levels configuration
graph = create_graph(selected_levels)

# Display the graph
st.graphviz_chart(graph, use_container_width=True)


if st.button("Print Data"):
    data = student.get_student_graph_data()

# # Display scores as text
# st.write(f'Scores for {student.name}:')
# tests = get_student_tests(student.id)
#
# # Dropdown of tests
# test = st.selectbox('Select a test', tests, format_func=lambda test: test.test_name)
#
# test_evaluations = get_student_test_evaluations(student.id, test.id)
# # Display scores as text
# st.success(f'Scores for {test.test_name}:')
# for evaluation in test_evaluations:
#     st.write(f'Category: {evaluation.get_test_competency().get_competency_type().type},
#     Score: {evaluation.score}, Comments: {evaluation.comments}')
#
# # Display evaluations
# evaluations = student.get_evaluations()
# st.success('Evaluations:')
# for evaluation in evaluations:
#     st.write(f'Category: {evaluation.get_test_competency().get_competency_type().type} Comments
#     {evaluation.comments} Score: {evaluation.score}')
#
#
#
# if 'grades' in st.session_state and 'question_categories' in st.session_state and
# st.session_state.grades:
#     # Convert grades to numeric values
#     grade_mapping = {'Bad': 1, 'Poor': 2, 'Good': 3, 'Excellent': 4}
#     test_categories_scores = {} # Format: {('Algebra', test_number): [scores], ...}
#
# # st.write(list())
# for item in get_student_tests(1):
#     print(item.test_name)


# if 'grades' in st.session_state and 'question_categories' in st.session_state and
# st.session_state.grades:
#     # Convert grades to numeric values
#     grade_mapping = {'Bad': 1, 'Poor': 2, 'Good': 3, 'Excellent': 4}
#     test_categories_scores = {} # Format: {('Algebra', test_number): [scores], ...}

#     # Populate test_categories_scores with grades, organized by category and test number
#     for (test_number, question_number), grade in st.session_state.grades.items():
#         category = st.session_state.question_categories.get((test_number, question_number))
#         if category: # If category exists for this question
#             key = (category, test_number)
#             if key not in test_categories_scores:
#                 test_categories_scores[key] = []
#             test_categories_scores[key].append(grade_mapping[grade])

#     # Calculate average score per category per test
#     category_scores = {} # Format: {'Algebra': {test_number: avg_score, ...}, ...}
#     for (category, test_number), scores in test_categories_scores.items():
#         if category not in category_scores:
#             category_scores[category] = {}
#         category_scores[category][test_number] = sum(scores) / len(scores)

#     # Plotting
#     plt.figure(figsize=(10, 6))
#     for category, scores in category_scores.items():
#         sorted_tests = sorted(scores.keys())
#         avg_scores = [scores[test] for test in sorted_tests]
#         plt.plot(sorted_tests, avg_scores, marker='o', label=category)

#     plt.title('Student Scores Over Tests by Category')
#     plt.xlabel('Test Number')
#     plt.ylabel('Average Score')
#     plt.legend(title='Category')
#     plt.grid(True)
#     st.pyplot(plt)
# else:
#     st.write('No grades available to display.')
