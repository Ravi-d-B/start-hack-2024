import streamlit as st

st.image('src/app/streamlit_app/logos/logo2.png', width=(400))




st.write('''DRUID is a revolutionary Primary School Teacher platform \n\nNow. Every student's progress can be monitored to help them fulfil their potential. \n\n With in-depth knowledge of the curriculum and student data, DRUID can make personalised teaching recommendations.''')


if st.button('Instructions', type="primary"):
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
