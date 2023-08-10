import streamlit_survey as ss
import streamlit as st
import pandas as pd

survey = ss.StreamlitSurvey()


st.title("Survey for Informative Priors")
st.write("This survey draft is realized with Python's Streamlit package by Sara Gironi. It is based on the paper ***Bayesian Impact Evaluation with Informative Priors*** by Leonardo Iacovone, David McKenzie and Rachael Meager.")
st.write("""The scope of this survey is to record informative priors of different categories of actors: policymakers, experts and firms, in order to incorporate
them in Bayesian impact evaluation, which is particularly helpful to learn more from expensive new programs tested on relatively small samples.""")
st.write("The following questions regard the priors on a Colombian Government Program which aimed to increase export tested on a group of 200 firms.")

# Initialize session state
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'
    st.session_state['consent'] = False
    st.session_state['submit'] = False
    st.session_state['No answer'] = ''

df = pd.DataFrame()

def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    #return st.session_state['No answer']
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True

def add_submission():
    st.session_state['submit'] = True 


if 'data' not in st.session_state:
    st.session_state['data'] = {
    'Professional Category': [],
    'Prior on the program\'s impact': [],
    'Percentage of expected impact': [],
    'Probability of expected impact': [],
    'Effects of the impact': [],
    'Motivation': []
}

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

if st.session_state['consent']:
    st.write("Specify your professional category:")
    option = st.selectbox(
        'Select one of the options below:',
        ('Policymaker', 'Expert', 'Firm'))
    
    if 'option' not in st.session_state:
        st.session_state.option = option

    # Update the selected choice if a new option is selected
    if option != st.session_state.option:
        st.session_state.option = option

    
    st.write("Express your beliefs regarding the impact of the consulting programm on export for the firms offered the treatment compared to firms offered just the diagnostic phase and trade:")
    export_impact = st.radio("Select one of the options below:", options=["Positive", "Negative", "No changes"], horizontal=False, key = 'export_impact')

    if 'export_impact' not in st.session_state:
        st.session_state.export_impact = export_impact

    # Update the selected choice if a new option is selected
    if export_impact != st.session_state.export_impact:
        st.session_state.export_impact = export_impact

    if export_impact == "Positive":
        st.write("""Choose what percentage on average do you think the export is going to increase in the treated firms:""")
        positive_slider = st.slider("Select the percentage sliding on the bar below:", 0, 100, format = '%d', key = 'positive_slider')

        if 'positive_slider' not in st.session_state:
            st.session_state.positive_slider = positive_slider

        # Update the selected choice if a new option is selected
        if positive_slider != st.session_state.positive_slider:
            st.session_state.positive_slider = positive_slider

        st.write("""Choose with what probability on average do you think the export is going to increase in the treated firms:""")
        prob_slider = st.slider("Select the probability sliding on the bar below:", 0, 100, key = 'prob_slider')

        if 'prob_slider' not in st.session_state:
            st.session_state.prob_slider = prob_slider

        # Update the selected choice if a new option is selected
        if prob_slider != st.session_state.prob_slider:
            st.session_state.prob_slider = prob_slider

        st.write("Please shortly summarize the reasons for your previous answer:")
        positive_text = st.text_input("Write your answer below:", key = 'positive_text' )

        if 'positive_text' not in st.session_state:
            st.session_state.positive_text = positive_text

        # Update the selected choice if a new option is selected
        if positive_text != st.session_state.positive_text:
            st.session_state.positive_text = positive_text

        export_outcome = st.radio("Select one of the following options", options = ["Diversify the range of products exported", "Diversify the destinations of exportation", "All of the above"], key = 'export_outcome')
    
        if 'export_outcome' not in st.session_state:
            st.session_state.export_outcome = export_impact

        # Update the selected choice if a new option is selected
        if export_outcome != st.session_state.export_outcome:
            st.session_state.export_outcome = export_outcome

    elif export_impact == "Negative":
        st.write("""Choose what percentage on average do you think the export is going to decrease in the treated firms:""")
        negative_slider = st.slider("Select the percentage sliding on the bar below:", -100, 0, format = '%f', key = 'negative_slider')

        if 'negative_slider' not in st.session_state:
            st.session_state.negative_slider = negative_slider

        # Update the selected choice if a new option is selected
        if negative_slider != st.session_state.negative_slider:
            st.session_state.negative_slider = negative_slider

        st.write("""Choose with what probability on average do you think the export is going to decrease in the treated firms:""")
        prob_slider_neg = st.slider("Select the probability sliding on the bar below:", 0, 100, key = 'prob_slider_neg')

        if 'prob_slider_neg' not in st.session_state:
            st.session_state.prob_slider_neg = prob_slider_neg

                # Update the selected choice if a new option is selected
        if prob_slider_neg != st.session_state.prob_slider_neg:
            st.session_state.prob_slider_neg = prob_slider_neg

        st.write("Please shortly summarize the reasons for your previous answer:")
        negative_text = st.text_input("Write your answer below:", key = 'negative_text')

        if 'negative_text' not in st.session_state:
            st.session_state.negative_text = negative_text

                    # Update the selected choice if a new option is selected
        if negative_text != st.session_state.negative_text:
            st.session_state.negative_text = negative_text
    else: 
        st.write("""Choose with what probability on average do you think the export is not going to change in the treated firms:""")
        prob_slider_neutral = st.slider("Select the probability sliding on the bar below:", 0, 100, key = 'prob_slider_neutral')
        
        if 'prob_slider_neutral' not in st.session_state:
            st.session_state.prob_slider_neutral = prob_slider_neutral
        # Update the selected choice if a new option is selected
        if prob_slider_neutral != st.session_state.prob_slider_neutral:
            st.session_state.prob_slider_neutral = prob_slider_neutral

        st.write("Please shortly summarize the reasons for your previous answer:")
        text = st.text_input("Write your answer below:", key = 'text')

        if 'text' not in st.session_state:
            st.session_state.text = text

            # Update the selected choice if a new option is selected
        if text != st.session_state.text:
            st.session_state.text = text

    submit = st.button("Submit", on_click = add_submission)

    if st.session_state['submit']:
        st.success("You completed the form successfully!")
    
        # Save session state in a CSV file
        data = {
            'Professional Category': [safe_var("option")],
            'Prior on the program\'s impact': [safe_var("export_impact")],
            'Percentage of expected impact': [safe_var("positive_slider"), safe_var("negative_slider")],
            'Probability of expected impact': [safe_var("prob_slider"), safe_var("prob_slider_neg"), safe_var("prob_slider_neutral")],
            'Effects of the impact': [safe_var("export_outcome")],
            'Motivation' : [safe_var("positive_text"), safe_var("negative_text"), safe_var("text")]

        }

        #st.write(data)

            #st.write(st.session_state)

        # Append session state data to the CSV file
        data = st.session_state['data']
        max_length = max(len(data[key]) for key in data)
        data_filled = {key: data[key] + [''] * (max_length - len(data[key])) for key in data}
        df = pd.DataFrame(data_filled)
        df.to_csv('Results.csv', index=False)

    # ...

    def add_submission():
        data = st.session_state['data']
        data['Professional Category'].append(safe_var('option'))
        data['Prior on the program\'s impact'].append(safe_var('export_impact'))

        if safe_var('export_impact') == 'Positive':
            data['Percentage of expected impact'].append(safe_var('positive_slider'))
            data['Probability of expected impact'].append(safe_var('prob_slider'))
            data['Effects of the impact'].append(safe_var('export_outcome'))
            data['Motivation'].append(safe_var('positive_text'))
        elif safe_var('export_impact') == 'Negative':
            data['Percentage of expected impact'].append(safe_var('negative_slider'))
            data['Probability of expected impact'].append(safe_var('prob_slider_neg'))
            data['Effects of the impact'].append(safe_var('export_outcome'))
            data['Motivation'].append(safe_var('negative_text'))
        else:
            data['Percentage of expected impact'].append(None)
            data['Probability of expected impact'].append(safe_var('prob_slider_neutral'))
            data['Effects of the impact'].append(None)
            data['Motivation'].append(safe_var('text'))

        st.session_state['data'] = data

        df = pd.DataFrame(data)
        df.to_csv('Results.csv', index=False)