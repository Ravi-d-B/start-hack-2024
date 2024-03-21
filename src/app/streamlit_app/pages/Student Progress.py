import streamlit as st

from app.streamlit_app.database import get_all_test_competency_types
from app.data.competencies import get_all_subjects

subjects = get_all_subjects()
if 'subject' not in st.session_state:
    st.session_state.subject = subjects[0]

# Initialize selected_competencies in session_state if not present
if 'selected_competencies' not in st.session_state:
    st.session_state.selected_competencies = []

# Subject selection
st.session_state.subject = st.selectbox("Select a subject", subjects,
                                        index=subjects.index(st.session_state.subject))

competencies = sorted(get_all_test_competency_types(), key=lambda x: x.code)

for comp in competencies:
    if comp.code.startswith(st.session_state.subject):
        # Generate a unique key for each checkbox to prevent conflicts
        unique_key = f"checkbox_{comp.code}"

        # Determine if this competency is currently selected
        is_selected = unique_key in st.session_state.selected_competencies

        # Create the checkbox, setting it to the current state of selection
        current_selection = st.checkbox(f'{comp.code} - {comp.type}', value=is_selected,
                                        key=unique_key)

        # Update the session state based on the checkbox interaction
        if current_selection and unique_key not in st.session_state.selected_competencies:
            st.session_state.selected_competencies.append(unique_key)
        elif not current_selection and unique_key in st.session_state.selected_competencies:
            st.session_state.selected_competencies.remove(unique_key)
