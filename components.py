import streamlit as st
import plotly
from utils import *
import streamlit.components.v1 as components

def consent_form():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Consent", expanded=True):
            st.markdown("""
            By submitting the form below you agree to your data being used for research purposes. 
            """)
            agree = st.checkbox("I understand and consent.")
            if agree:
                st.markdown(f'''Thank you for giving your consent. Select \"Next\" to start the survey.''')
                st.button('Next', on_click=add_consent)


def user_full_name():
    st.text_input("Please write your full name and surname:", key = 'user_full_name')

def user_position():
    st.text_input("Please write your working position:", key = 'user_position')

def user_professional_category():
    # Professional Category Checkbox
    st.selectbox('Specify your professional category. Please click below to see all available options:', ('Policymaker', 'Academic/Researcher', 'Entrepreneur/Manager'), key="professional_category")

def personal_information():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Personal Information", expanded=True):
            user_full_name()
            user_position()
            user_professional_category()
