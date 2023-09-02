import streamlit_survey as ss
import streamlit as st
import pandas as pd
from utils import *
from components import *
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(layout="wide")
survey = ss.StreamlitSurvey()


# Initialize session state
initialize_session_state()

# Show introductory texts
show_titles_and_subtitles()

# Request of consent
consent_form()

if st.session_state['consent']:

    personal_information()

    instructions()

    instructions_table()

    first_question()

    new_bins_df, fig, bins_grid = first_question_grid()

    #table_graph_position(bins_grid, fig)

    st.write(SUBTITLE_QUESTION_1_2)
    st.number_input('Click to increase or decrease the counter.', min_value=0, max_value=100, key = 'input_question_1')
    

    
    #st.radio(EXPORT_IMPACT_DESCRIPTION, options=["Positive", "Negative", "No changes"], horizontal=False, key = 'export_impact')

    #percentage_of_expected_impact(st.session_state.export_impact)
    #probability_of_expected_impact(st.session_state.export_impact)
    #motivation()

    #if st.session_state.export_impact == "Positive":
    #    st.radio("Select one of the following options", options = ["Diversify the range of products exported", "Diversify the destinations of exportation", "All of the above"], key = 'export_outcome')

    
    submit = st.button("Submit", on_click = add_submission, args = (new_bins_df, ))

    if st.session_state['submit']:
        
        st.success("Thank you for completing the Academic Prior Beliefs Elicitation Survey!")

