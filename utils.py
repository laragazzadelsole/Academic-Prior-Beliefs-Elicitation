
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
import streamlit.components.v1 as components

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

# BEGINNING OF THE SURVEY

def first_question():
    st.subheader(TITLE_QUESTION_1)
    st.write(SUBTITLE_QUESTION_1)


def first_question_grid():
    st.write('BELIEFS ABOUT THE IMPACT ON THE NUMBER OF PRODUCTS THAT FIRMS EXPORT')

    bins_df = pd.read_excel('Probability Bins.xlsx', header = 0)
    bins = bins_df['Probability']


    data_container = st.container()

    with data_container:
        table, plot = st.columns(2)
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
            #components.html(grid_return["data"].to_html(escape=False), height=400, scrolling=True)


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
        # Display the distribution of probabilities with a bar chart 
        
            fig, ax = plt.subplots()
            ax.bar(bins, bins_grid['Percentage'])
            ax.set_xlabel('Probability Bins')
            ax.set_ylabel('Percentage of Beliefs')
            ax.set_title('Distribution of Beliefs about the Impact on the Number of Products that Firms Export')
            ax.set_xticks(bins)
            ax.set_xticklabels(bins, rotation=80)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

    new_bins_df = pd.DataFrame(bins_grid.T)
    #new_bins_df.to_csv('Export beliefs.csv', index=False)

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
    session_state_df = pd.DataFrame(data)
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
    

    