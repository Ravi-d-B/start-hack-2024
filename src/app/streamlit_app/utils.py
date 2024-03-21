from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

def client():
    return OpenAI(api_key=openai_api_key)
    
def get_prompt_template(id, information):
    # Initialise chat history
    if id not in st.session_state:
        st.session_state.id = [
            {
                'role': 'system',
                'content': f'''
                You are a primary school teacher assistant. 
                Your role is to suggest where a student needs support based on previous test results.
                Please summarise the current progress and suggest areas for improvement.
                The evaluations shouldn't be graded but rather evaluated. These are the evaluations in german but should be given in english:
                1: Das Klappt noch nicht
                2: Das Gelingt mit teilweise
                3: Das kann ich gut
                4: Das kann ich sehr gut

                This is the student profile {information}.
                You should always give recommendations for Further Support:
                '''
                }
                ]
        return st.session_state.id
    else:
        return st.session_state.id
        