import streamlit as st

# Path to your local image
image_path = 'src/app/streamlit_app/logos/logo2.png'

# Create a 3-column layout
col1, col2, col3 = st.columns([1,2,2])

# Display the image in the middle column
with col2:
    st.image(image_path, width=400)

text = '''
DRUID is a revolutionary Primary School Teacher platform!\n\n
Now, every student's progress can be monitored to help them fulfil their potential.\n
With in-depth knowledge of the curriculum and student data, DRUID can make personalised teaching recommendations.
'''

# Using st.markdown with HTML for centering the text
st.markdown(f"<div style='text-align: center;'>{text}</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Upload your test")
    st.image('src/app/streamlit_app/images/upload.jpg')

with col2:
    st.subheader("2. Grade your test")
    st.image('src/app/streamlit_app/images/teacher.jpg')

with col3:
    st.subheader("3. Track with AI")
    st.image('src/app/streamlit_app/images/graph.png')
