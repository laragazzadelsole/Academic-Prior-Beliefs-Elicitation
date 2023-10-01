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

    url = "https://raw.githubusercontent.com/laragazzadelsole/Academic-Prior-Beliefs-Elicitation/dev2/probability_bins.csv" 
    download = requests.get(url).content

    # Reading the downloaded content and turning it into a pandas dataframe

    bins_df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    #bins_df = pd.read_csv('probability_bins.csv', header = 0)
    
    bins = bins_df['Probability']
    st.write(bins)

    new_bins_df, fig, bins_grid = first_question_grid(bins_df, bins) 

    #table_graph_position(bins_grid, fig)

    st.write(SUBTITLE_QUESTION_1_2)
    st.number_input('Click to increase or decrease the counter.', min_value=0, max_value=10000, key = 'input_question_1')
        
    submit = st.button("Submit", on_click = add_submission, args = (new_bins_df, ))

    if st.session_state['submit']:
        
        st.success("Thank you for completing the Academic Prior Beliefs Elicitation Survey!")

