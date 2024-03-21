from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def initialise_openai_client(api_key):
    try:
        client = OpenAI(api_key=api_key)
        return client
    except KeyError:
        return None
    
def get_prompt_template(id, questions, solutions):
    # Initialise chat history
    if id not in st.session_state:
        st.session_state.id = [
            {
                'role': 'system',
                'content': f'''
                You are a primary school elementary teacher assistant. 
                Your role is to suggest where a student needs support based on previous test results. 
                '''
                }
                ]
        return st.session_state.id
    else:
        return st.session_state.id
        
    