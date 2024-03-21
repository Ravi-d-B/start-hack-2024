# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt


st.title('Student Category Scores Over Tests')

if 'grades' in st.session_state and 'question_categories' in st.session_state and st.session_state.grades:
    # Convert grades to numeric values
    grade_mapping = {'Bad': 1, 'Poor': 2, 'Good': 3, 'Excellent': 4}
    test_categories_scores = {} # Format: {('Algebra', test_number): [scores], ...}

    # Populate test_categories_scores with grades, organized by category and test number
    for (test_number, question_number), grade in st.session_state.grades.items():
        category = st.session_state.question_categories.get((test_number, question_number))
        if category: # If category exists for this question
            key = (category, test_number)
            if key not in test_categories_scores:
                test_categories_scores[key] = []
            test_categories_scores[key].append(grade_mapping[grade])

    # Calculate average score per category per test
    category_scores = {} # Format: {'Algebra': {test_number: avg_score, ...}, ...}
    for (category, test_number), scores in test_categories_scores.items():
        if category not in category_scores:
            category_scores[category] = {}
        category_scores[category][test_number] = sum(scores) / len(scores)

    # Plotting
    plt.figure(figsize=(10, 6))
    for category, scores in category_scores.items():
        sorted_tests = sorted(scores.keys())
        avg_scores = [scores[test] for test in sorted_tests]
        plt.plot(sorted_tests, avg_scores, marker='o', label=category)

    plt.title('Student Scores Over Tests by Category')
    plt.xlabel('Test Number')
    plt.ylabel('Average Score')
    plt.legend(title='Category')
    plt.grid(True)
    st.pyplot(plt)
else:
    st.write('No grades available to display.')