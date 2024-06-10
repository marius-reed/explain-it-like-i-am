import streamlit as st
from model import query_model
from upload_to_databricks_table import write_file_to_delta_table
import os
from dotenv import load_dotenv


load_dotenv()




personas_dict = {
    "Rocket Scientist":"rocket_scientist", 
    "Developer":"developer", 
    "10 Year old":"10_year_old", 
    "Golden Retreiver":"golden_retriver", 
    "CEO":"ceo"}


with st.container(border=True):
    # Add title
    st.markdown("<h1 style='text-align: center;'>Explain it to me as I am a... 🚀</h1>", unsafe_allow_html=True)

    # Add subtitle
    st.markdown("<h3 style='text-align: center; color: gray;'>The 'no-shame-application' to figure out what really happened in that meeting you missed! 🤔 Upload the meeting minutes and ask what happend!</h3>", unsafe_allow_html=True)


# Sidebar layout
st.sidebar.header('I am a:')
profession_input = st.sidebar.selectbox(
    'Select a profession:',
    ('Rocket Scientist', 'Developer', '10 Year old', 'Golden Retreiver', 'CEO')
)


# Display the selected profession
st.sidebar.write(f'You selected: {profession_input}.')

profession = personas_dict[profession_input]


proffesion_to_pic = {"rocket_scientist":"scientist.jpg","developer":"developer.jpg", "10_year_old":"baby_emoji.jpg", "golden_retriver":"GR.jpg", "ceo":"bb.jpg"}


#diaply image of persona
st.sidebar.image(f"assets/{proffesion_to_pic[profession]}", use_column_width=True)

# File upload in the sidebar
st.sidebar.header('Upload you meeting minutes:')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "txt", "xlsx"])
table_name = "workspace.meetings.notes"
write_file_to_delta_table(uploaded_file, table_name)


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def add_message():
    user_message = st.session_state.user_input
    st.session_state.chat_history = []
    st.session_state.chat_history.append(user_message)
    # Placeholder for a response (Here you can add logic for bot responses)
    query_result = query_model(profession, user_message)
    st.session_state.chat_history.append(query_result)
    st.session_state.user_input = ''  # Clear the input after sending


st.text_input("Type your message here...", key="user_input", on_change=add_message)
st.text_area("This happened in your meeting", value="\n".join(st.session_state.chat_history), height=300, key="chat_display", disabled=True)



# Main content area
st.header("File upload")

if uploaded_file is not None:
    # Process the uploaded file (you can add your file processing logic here)
    st.write("File uploaded successfully!")
    st.write(uploaded_file)
else:
    st.write("No file uploaded yet.")