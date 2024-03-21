# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt


st.title('Student Category Scores Over Tests')

if 'grades' in st.session_state and st.session_state.grades:
    # Convert grades to numeric values for plotting
    grade_mapping = {'Bad': 1, 'Poor': 2, 'Good': 3, 'Excellent': 4}
    scores = {test: grade_mapping[grade] for (test, _), grade in st.session_state.grades.items()}
    
    # Simple line plot of scores
    plt.figure()
    plt.plot(list(scores.keys()), list(scores.values()), marker='o')
    plt.title('Scores Over Tests')
    plt.xlabel('Test Number')
    plt.ylabel('Score')
    plt.grid(True)
    st.pyplot(plt)
else:
    st.write('No grades available to display.')
