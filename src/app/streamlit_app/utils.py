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
                You are a primary school elementary teacher assistant. 
                Your role is to suggest where a student needs support based on previous test results. 
                This is the student profile {information}.
                '''
                }
                ]
        return st.session_state.id
    else:
        return st.session_state.id
        