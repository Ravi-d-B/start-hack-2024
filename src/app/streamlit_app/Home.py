import streamlit as st

st.sidebar.image('src/app/streamlit_app/logos/logo_trans.png')

st.markdown("<h1 style='text-align: center; font-family: Alexandria; font-size: 100px ;color: #27b1b1;'>DRUID</h1>", unsafe_allow_html=True)

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
