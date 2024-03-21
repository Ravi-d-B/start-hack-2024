# Function to display scores as a line plot
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from app.streamlit_app.database import get_student_tests
from app.streamlit_app.utils import get_prompt_template, client

from app.streamlit_app.database import (
    get_students, get_student_tests,
    get_student_test_evaluations, get_all_student_test_evaluations
)

from app.data.competencies import get_all_subjects, get_compentencies_for_subject_code, get_full_comp_df

from app.streamlit_app.graph import create_graph
plt.rcParams['font.size'] = 20

# set font to Arial
plt.rcParams['font.sans-serif'] = 'Arial'

# Set the font globally
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']  # Or any font you like


st.title('Student Progression')


def plot_results(df):
    if df.empty:
        st.write("No data to display")
        return
    # Count number of unique concatenated categories
    cats = (df['cat1'] + df['cat2']).unique()
    num_cats = len(cats)

    # Calculate rows for n x 2 layout, rounding up. Ensure at least 1 row.
    num_rows = max(np.ceil(num_cats / 2).astype(int), 1)

    # Create subplots in a n x 2 layout, adjusting for when num_cats is 1 or 2
    if num_cats <= 2:
        fig, axs = plt.subplots(num_rows, num_cats, figsize=(10 * num_cats, 5 * num_rows),
                                sharex=False, sharey=True)
        # Ensure axs is 2-dimensional
        axs = np.atleast_2d(axs)
    else:
        fig, axs = plt.subplots(num_rows, 2, figsize=(30, 7 * num_rows), sharex=False,
                                sharey=True)

    # Flatten the axs array to simplify indexing
    axs = axs.flatten()


    for i, cat_val in enumerate(cats):
        # Filter on concatenated categories
        df_cat = df.query('(cat1 + cat2) == @cat_val')

        title_part_1 = df_cat['code'].iloc[0].rsplit('.', 2)[0:2]
        title_part_2 = df_cat['code'].iloc[0].rsplit('.', 1)[0]
        # Assuming get_full_comp_df() function fetches a DataFrame with 'code' and 'bezeichnung' columns
        title_part_1 = get_full_comp_df().query('code == @title_part_1')['bezeichnung'].iloc[0]
        title_part_2 = get_full_comp_df().query('code == @title_part_2')['bezeichnung'].iloc[0]

        # Set title with the parts from the code
        axs[i].set_title(f'{title_part_1} - {title_part_2}', pad=20)

        # Make a line for every cat3
        for cat3 in df_cat['cat3'].unique():
            df_cat3 = df_cat.query('cat3 == @cat3')
            axs[i].plot(df_cat3['test_date'], df_cat3['score'],
                        marker='o',
                        label=df_cat3['code'].iloc[0])
        axs[i].legend()
        axs[i].set_facecolor('#f0f0f0')
        for side in ['top', 'bottom', 'left', 'right']:
            axs[i].spines[side].set(lw=2)

        # make line thicker
        axs[i].lines[0].set_linewidth(3)
        axs[i].set_yticks([0, 1, 2, 3, 4, 5])
        axs[i].set_yticklabels(['',
                                'Das Klappt noch nicht',
                                'Das Gelingt mit teilweise',
                                'Das kann ich gut',
                                'Das kann ich sehr gut',
                                ''])

    # If num_cats is odd and greater than 2, hide the last subplot
    if num_cats % 2 != 0 and num_cats > 2:
        fig.delaxes(axs[-1])

    plt.tight_layout()
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


information = student.get_student_graph_data()

if id not in st.session_state or id is not st.session_state.id:
    st.session_state[id] = get_prompt_template(student.name, information)
prompt_template = st.session_state[id]

# Display chat messages from history on app rerun
for message in prompt_template:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

client = client()

if st.button("Ask AI for a student progress summary"):

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in prompt_template
            ],
            temperature=0.2,
            stream=True
        )
        response = st.write_stream(stream)
    prompt_template.append({"role": "assistant", "content": response})
