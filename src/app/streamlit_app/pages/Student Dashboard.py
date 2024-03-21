# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt
from app.streamlit_app.database import get_student_tests

from app.streamlit_app.database import get_students, get_student_tests, get_student_test_evaluations, get_all_student_test_evaluations

# st.title('Student Category Scores Over Tests')

<<<<<<< HEAD
=======
students = get_students()
# Dropdown of students
student = st.selectbox('Select a student', students, format_func=lambda student: student.name)

# Display scores as text
st.write(f'Scores for {student.name}:')
tests = get_student_tests(student.id)

# Dropdown of tests
test = st.selectbox('Select a test', tests, format_func=lambda test: test.test_name)

test_evaluations = get_student_test_evaluations(student.id, test.id)
# Display scores as text
st.success(f'Scores for {test.test_name}:')
for evaluation in test_evaluations:
    st.write(f'Category: {evaluation.get_test_competency().get_competency_type().type}, Score: {evaluation.score}, Comments: {evaluation.comments}')

# Display evaluations
evaluations = student.get_evaluations()
st.success('Evaluations:')
for evaluation in evaluations:
    st.write(f'Category: {evaluation.get_test_competency().get_competency_type().type} Comments {evaluation.comments} Score: {evaluation.score}')

if 'grades' in st.session_state and 'question_categories' in st.session_state and st.session_state.grades:
    # Convert grades to numeric values
    grade_mapping = {'Bad': 1, 'Poor': 2, 'Good': 3, 'Excellent': 4}
    test_categories_scores = {} # Format: {('Algebra', test_number): [scores], ...}
>>>>>>> 4e1638dfd0f67a431c8eea029127953ccab546e7

# st.write(list())
for item in get_student_tests(1):
    print(item.test_name)


# if 'grades' in st.session_state and 'question_categories' in st.session_state and st.session_state.grades:
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