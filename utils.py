
import streamlit as st
from constants import *
import pandas as pd
#from google.oauth2 import service_account
#import gsheetsdb
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import AgGrid, GridOptionsBuilder






# Uncomment if you want to create a new spreadsheet each time 
#testsheet = client.create('Test')
#testsheet.share('sara.gironi97@gmail.com', perm_type = 'user', role = 'writer')



# SURVEY

def show_titles_and_subtitles():
    st.title(TITLE)  
    st.write(SUBTITLE_1)
    st.write(SUBTITLE_2)
    st.write(SUBTITLE_3)

def first_question():
    st.subheader(TITLE_QUESTION_1)
    st.write(SUBTITLE_QUESTION_1)

def first_question_grid():

    bins_df = pd.read_excel('Probability Bins.xlsx', header = 0)

    # set only one column to be editable 
    grid_options = {
        "columnDefs": [
            {
                "headerName": "Probability",
                "field": "Probability",
                "editable": False,
            },
            {
                "headerName": "Percentage",
                "field": "Percentage",
                "editable": True,
            },
        ],
    }

    grid_return = AgGrid(bins_df, grid_options, fit_columns_on_grid_load = True)
    new_bins_df = grid_return["data"]
    new_bins_df = pd.DataFrame(new_bins_df)
    new_bins_df.to_csv('Export beliefs.csv', index=False)



def initialize_session_state():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
    
    if 'data' not in st.session_state:
        st.session_state['data'] = {
            'Professional Category': [],
            'Prior on the program\'s impact': [],
            'Percentage of expected impact': [],
            'Probability of expected impact': [],
            'Effects of the impact': [],
            'Motivation': []
        }

def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    #return st.session_state['No answer']
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True

def add_submission():
    st.session_state['submit'] = True 

    data = st.session_state['data']
    #data['Professional Category'].append(safe_var('professional_category'))
    #data['Prior on the program\'s impact'].append(safe_var('export_impact'))
    #data['Effects of the impact'].append(safe_var('export_outcome'))
    #data['Probability of expected impact'].append(safe_var('probability_of_expected_impact'))
    #data['Percentage of expected impact'].append(safe_var('percentage_of_expected_impact'))
    #data['Motivation'].append(safe_var('motivation_text'))
            
    st.session_state['data'] = data
    df = pd.DataFrame(data)
    #df.to_csv('Results.csv', index=False)


#Save the data in the spreadsheet in drive named 'Academic Prior Beliefs Elicitation Data'

scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']


def secrets_to_json():
 return {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json())
    
client = gspread.authorize(credentials)

sheet = client.open('Academic Prior Beliefs Elicitation Data').sheet1
#sheet.share('sara.gironi97@gmail.com', perm_type = 'user', role = 'writer')
sheet_updated = sheet.update([first_question_grid().columns.values.tolist()])
sheet = sheet.append_rows(first_question_grid().values.tolist())

    # Failures to append data to the same file 

    #sheet_updated = sheet.update([df.columns.values.tolist()])
    #new_val = df.values.tolist()
    #sheet_updated.append_row(new_val, value_input_option='RAW')

    