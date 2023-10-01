
import streamlit as st
from datetime import datetime
from constants import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import streamlit.components.v1 as components
import requests
import io

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
            'Minimum Effect Size': [],
            'User Full Name': [],
            'User Working Position': [],
            'User Professional Category': []
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    #return st.session_state['No answer']
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True

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


# BEGINNING OF THE SURVEY

def instructions():
    st.subheader(TITLE_INSTRUCTIONS)
    st.write(SUBTITLE_INSTRUCTIONS)

def instructions_table():

# Create some example data
    data_container = st.container()

    with data_container:
        table, plot = st.columns([0.4, 0.6], gap = "large")
        with table:
            # Create Streamlit app
            st.subheader("Temperature Forecast Tomorrow in Your City")
            st.write('Please scroll on the table to see all available options.')

            # Define Ag-Grid options
            gb = GridOptionsBuilder()
            gb.configure_column("Temperature", editable=False, resizable=True)
            gb.configure_column("Probability", editable=False, resizable=True)

            # Create some example data as a Pandas DataFrame
            values_column = list(range(10, 31))
            zeros_column = [0 for _ in values_column]
            data = {'Temperature': values_column, 'Probability': zeros_column}
            df = pd.DataFrame(data)

            df.at[0, "Temperature"] = '< 10'
            df.at[20, "Temperature"] = '> 30'
            df.at[13, "Probability"] = 5
            df.at[14, "Probability"] = 15
            df.at[15, "Probability"] = 45
            df.at[16, "Probability"] = 20
            df.at[17, "Probability"] = 15

            df['Temperature'] = df['Temperature'].astype('str')


            # Initialize Ag-Grid
            grid_return = AgGrid(df, gridOptions=gb.build(), height=400, fit_columns_on_grid_load=True)
            bins_grid = grid_return["data"]
        
        with plot:
        # Display the distribution of probabilities with a bar chart 
            fig, ax = plt.subplots(figsize=(4, 3))  # Adjust the figure size as needed

            # Your data plotting code
            ax.bar(bins_grid['Temperature'], bins_grid['Probability'])
            ax.set_xlabel('Temperature', fontsize=8)  # Adjust fontsize as needed
            ax.set_ylabel('Probability', fontsize=8)  # Adjust fontsize as needed
            ax.set_title("Probability Distribution over Tomorrow's Temperatures", fontsize=9)  # Adjust fontsize as needed
            ax.set_xticks(df['Temperature'])
            ax.set_xticklabels(df['Temperature'], fontsize=6)  # Adjust fontsize as needed
            ax.set_yticks(df['Probability'])
            ax.set_yticklabels(df['Probability'], fontsize=7)
            plt.tight_layout()

            # Adjust the title and labels proportions
            fig.subplots_adjust(top=0.9, right=0.95)  # Adjust the values as needed

            st.pyplot(fig, use_container_width=False)

    st.write(CAPTION_INSTRUCTIONS)

def first_question():
    st.subheader(TITLE_QUESTION_1)
    st.write(SUBTITLE_QUESTION_1)


def first_question_grid():
    st.subheader('Beliefs about the Impact on the Number of Products that Firms Export')
    st.write('Please scroll on the table to see all available options.')
        
    # Downloading the csv file from your GitHub account

    url = "https://raw.githubusercontent.com/laragazzadelsole/Academic-Prior-Beliefs-Elicitation/dev2/probability_bins.csv" 
    download = requests.get(url).content

    # Reading the downloaded content and turning it into a pandas dataframe

    bins_df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    #bins_df = pd.read_csv('probability_bins.csv', header = 0)
    
    bins = bins_df['Probability']

    data_container = st.container()

    with data_container:
        table, plot = st.columns([0.4, 0.6], gap = "large")
        with table:

            # Set up Ag-Grid options
            gb = GridOptionsBuilder()
            gb.configure_column("Probability", editable=False, resizable=True)
            gb.configure_column("Percentage", editable=True, resizable=True)

            # Initialize Ag-Grid
            grid_return = AgGrid(bins_df, gridOptions=gb.build(), height=400, fit_columns_on_grid_load = True, update_mode=GridUpdateMode.VALUE_CHANGED)

            # Get the modified data from Ag-Grid
            bins_grid = grid_return["data"]
            #st_aggrid(bins_grid, height=400, fit_columns_on_grid_load=True)

            # Initialize the counter
            total_percentage = 100
            # Calculate the new total sum
            percentage_inserted = sum(bins_grid['Percentage'])
            # Calculate the difference in sum
            percentage_difference = total_percentage - percentage_inserted

            # Update the counter
            total_percentage = percentage_difference

        
            # Display the counter

            if percentage_difference >= 0:
                st.write(f"**You still have to allocate {percentage_difference} percent probability.**")
            else:
                st.write(f'**:red[You have inserted {abs(percentage_difference)} percent more, please review your percentage distribution.]**')

        with plot:
            fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figure size as needed

            # Your data plotting code
            ax.bar(bins, bins_grid['Percentage'])
            ax.set_xlabel('Probability Bins', fontsize=14)  # Adjust fontsize as needed
            ax.set_ylabel('Percentage of Beliefs', fontsize=14)  # Adjust fontsize as needed
            ax.set_title('Distribution of Beliefs about the Impact on the Number of Products that Firms Export', fontsize=16)  # Adjust fontsize as needed
            ax.set_xticks(bins)
            ax.set_xticklabels(bins, rotation=80, fontsize=10)  # Adjust fontsize as needed

            plt.tight_layout()

            # Adjust the title, labels, and plot proportions
            fig.subplots_adjust(top=0.9, right=0.95)  # Adjust the values as needed

            st.pyplot(fig, use_container_width=True)
        # Display the distribution of probabilities with a bar chart 

    new_bins_df = pd.DataFrame(bins_grid.T)

    return new_bins_df, fig, bins_grid


def add_submission(new_bins_df):
    st.session_state['submit'] = True 
    
    # Update session state
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'
    MIN_EFF_SIZE = 'Minimum Effect Size'

    data[MIN_EFF_SIZE].append(safe_var('input_question_1'))
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))
            
    st.session_state['data'] = data
    
    new_bins_df[MIN_EFF_SIZE] =  [MIN_EFF_SIZE, data[MIN_EFF_SIZE][0]]
    new_bins_df[USER_FULL_NAME] = [USER_FULL_NAME, data[USER_FULL_NAME][0]]
    new_bins_df[USER_POSITION] = [USER_POSITION, data[USER_POSITION][0]]
    new_bins_df[USER_PROF_CATEGORY] = [USER_PROF_CATEGORY, data[USER_PROF_CATEGORY][0]]

    # Reorder the columns
    last_columns = new_bins_df.iloc[:, -3:]
    first_columns = new_bins_df.iloc[:, :-3]

    new_bins_df = pd.concat([last_columns, first_columns], axis=1)

    #save data to google sheet 
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    #creds = ServiceAccountCredentials.from_json_keyfile_name('prior-beliefs-elicitation-keys.json', scope)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json())
    client = gspread.authorize(creds)

    # Load the Google Sheet
    sheet = client.open("Academic Prior Beliefs Elicitation Data").sheet1

    #sheet_update = sheet.update([new_bins_df.columns.values.tolist()])
    sheet = sheet.append_rows([new_bins_df.values.tolist()[1]])
    #st.success('Data has been saved successfully.')
    
    #Navigate to the folder in Google Drive. Copy the Folder ID found in the URL. This is everything that comes after “folder/” in the URL. For example, if the URL was
    backup_sheet = client.create(f'Backup_{datetime.now()}_{data[USER_FULL_NAME]}', folder_id='1Pjz6JAf9MaVe_eSaAFpDhLFr4GMPj2jX').sheet1
    backup_sheet = backup_sheet.append_rows(new_bins_df.iloc[:2].values.tolist())
    #backup_sheet.share('sara.gironi97@gmail.com', perm_type = 'user', role = 'writer')
    

    