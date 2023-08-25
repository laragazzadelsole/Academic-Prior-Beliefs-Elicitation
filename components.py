import streamlit as st
import plotly
from utils import *
import streamlit.components.v1 as components

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


def user_full_name():
    st.text_input("Please write your full name and surname:", key = 'user_full_name')

def user_position():
    st.text_input("Please write your working position:", key = 'user_position')

def user_professional_category():
    # Professional Category Checkbox
    st.selectbox('Specify your professional category:', ('Policymaker', 'Expert', 'Entrepeneur'), key="professional_category")

def personal_information():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Personal Information", expanded=True):
            user_full_name()
            user_position()
            user_professional_category()
'''
def table_graph_position(bins_grid, fig):
    col1, col2 = st.beta_columns(2)

# Ag-Grid table in the first column
    with col1:
        components.html(bins_grid, height=400, scrolling=True)

# Histogram in the second column
    with col2:
        st.bar_chart(fig, use_container_width=True)
        data_container = st.container()


    #new_bins_df, fig = first_question_grid()
    with data_container:
        table, plot = st.columns(2)
        with table:
            bins_grid
        with plot:
            fig

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
     