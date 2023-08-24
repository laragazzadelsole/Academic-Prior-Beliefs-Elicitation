
import streamlit as st
from datetime import datetime
from constants import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# CONSENT PAGE

def show_titles_and_subtitles():
    st.title(TITLE)  
    st.write(SUBTITLE_1)
    st.write(SUBTITLE_2)
    st.write(SUBTITLE_3)


def initialize_session_state():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
       
    if 'data' not in st.session_state:
        st.session_state['data'] = {
            'Minimum Effect Size': []
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    #return st.session_state['No answer']
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True

# BEGINNING OF THE SURVEY

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
                "editable": False
            },
            {
                "headerName": "Percentage",
                "field": "Percentage",
                "editable": True
            }
        ]
    }

    # Initialize the counter
    total_percentage = 100
    hist_data = bins_df['Percentage']
    bins = bins_df['Probability']

    grid_return = AgGrid(bins_df, grid_options, fit_columns_on_grid_load = True, update_mode=GridUpdateMode.VALUE_CHANGED)
    new_bins_df = grid_return["data"]

    # Calculate the new total sum
    percentage_inserted = sum(new_bins_df['Percentage'])
    # Calculate the difference in sum
    percentage_difference = total_percentage - percentage_inserted

    # Update the counter
    total_percentage = percentage_difference

    hist_data = new_bins_df['Percentage']
    # Display the counter

    if percentage_difference >= 0:
        st.write(f"**You still have to allocate {percentage_difference} percent probability.**")
    else:
        st.write(f'**:red[You have inserted {abs(percentage_difference)} percent more, please review your percentage distribution.]**')

    
    # Display the distribution of probabilities with a bar chart 
    
    fig, ax = plt.subplots()
    ax.bar(bins, new_bins_df['Percentage'])
    ax.set_xlabel('Probability Bins')
    ax.set_ylabel('Percentage')
    ax.set_title('Bar Chart of Percentage Values')
    ax.set_xticks(bins)
    ax.set_xticklabels(bins, rotation=80)
    plt.tight_layout()
    st.pyplot(fig)

    new_bins_df = pd.DataFrame(new_bins_df.T)
    #new_bins_df.to_csv('Export beliefs.csv', index=False)

    return new_bins_df


def add_submission(new_bins_df):
    st.session_state['submit'] = True 
    
    # Update session state
    data = st.session_state['data']
    MIN_EFF_SIZE = 'Minimum Effect Size'

    data[MIN_EFF_SIZE].append(safe_var('input_question_1'))
            
    st.session_state['data'] = data
    minimum_effect_df = pd.DataFrame(data)
    new_bins_df[MIN_EFF_SIZE] =  [MIN_EFF_SIZE, data[MIN_EFF_SIZE][0]]
    #final_df = pd.concat([new_bins_df, minimum_effect_df], axis=1)
    st.write(minimum_effect_df)
    st.write(new_bins_df)

    #save data to google sheet 
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('prior-beliefs-elicitation-keys.json', scope)

    client = gspread.authorize(creds)

    # Load the Google Sheet
    sheet = client.open("Academic Prior Beliefs Elicitation Data").sheet1

    #sheet_update = sheet.update([new_bins_df.columns.values.tolist()])
    sheet = sheet.append_rows([new_bins_df.values.tolist()[1]])
    #st.success('Data has been saved successfully.')
    
    #Navigate to the folder in Google Drive. Copy the Folder ID found in the URL. This is everything that comes after “folder/” in the URL. For example, if the URL was
    backup_sheet = client.create(f'Backup_{datetime.now()}', folder_id='1Pjz6JAf9MaVe_eSaAFpDhLFr4GMPj2jX').sheet1
    backup_sheet = backup_sheet.append_rows(new_bins_df.iloc[:2].values.tolist())
    #backup_sheet.share('sara.gironi97@gmail.com', perm_type = 'user', role = 'writer')
    
    #CANCELLARE
    
#Save the data in the spreadsheet in drive named 'Academic Prior Beliefs Elicitation Data'
def secrets_to_json():
    return {
        "type": st.secrets["gcp_service_account"]["type"],
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






#client = gspread.authorize(credentials)

#sheet = client.open('Academic Prior Beliefs Elicitation Data').sheet1
#sheet.share('sara.gironi97@gmail.com', perm_type = 'user', role = 'writer')
#sheet_updated = sheet.update([first_question_grid().columns.values.tolist()])
#sheet = sheet.append_rows(first_question_grid().values.tolist())

    # Failures to append data to the same file 

    #sheet_updated = sheet.update([df.columns.values.tolist()])
    #new_val = df.values.tolist()
    #sheet_updated.append_row(new_val, value_input_option='RAW')

    