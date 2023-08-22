import streamlit as st
from utils import *


def consent_form():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Consent", expanded=True):
            st.markdown("""
            By submitting the form below you agree to your data being used for research. 
            """)
            agree = st.checkbox("I understand and consent.")
            if agree:
                st.markdown("You have consented. Select \"Next\" to start the survey.")
                st.button('Next', on_click=add_consent)

'''
def percentage_of_expected_impact(export_impact):
    if export_impact == "Positive":
        st.slider(PERC_EXPECTED_IMPACT_DESCRIPTION.format("increase"), 0, 100, format = '%d', key = 'percentage_of_expected_impact')
    elif export_impact == "Negative":
        st.slider(PERC_EXPECTED_IMPACT_DESCRIPTION.format("descrease"), -100, 0, format = '%d', key = 'percentage_of_expected_impact')
    else: 
        pass

def probability_of_expected_impact(export_impact):
    if export_impact == "Positive":
        st.slider(PROB_EXPECTED_IMPACT_DESCRIPTION.format("is going to increase"), 0, 100, key = 'probability_of_expected_impact')
    elif export_impact == "Negative":
        st.slider(PROB_EXPECTED_IMPACT_DESCRIPTION.format("is going to decrease"), 0, 100, key = 'probability_of_expected_impact')
    else: 
        st.slider(PROB_EXPECTED_IMPACT_DESCRIPTION.format("is not going to change"), 0, 100, key = 'probability_of_expected_impact')

def motivation():
    st.text_input("Please shortly summarize the reasons for your previous answer:", key = 'motivation_text')
'''
     