import streamlit as st
# from streamlit.components.v1 import iframe
import smtplib
import re
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
st.set_page_config(page_title="TZ'23 General Registration",page_icon="IETE_logo.png")
link_home = "**[Go to home page](https://technotronz23.wixsite.com/home)**"
e,w,r=st.columns([2,2, 1])
with r:
    st.markdown(link_home, unsafe_allow_html=True)
img = Image.open('TZ_logo.png')
st.image(img)
hide_ststyle = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_ststyle, unsafe_allow_html=True)
i_=0
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("technotronz23-general.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Registration").sheet1

p=st.empty()
one,two,thr=st.columns([0.1,1, 0.1])
with two:
    st.header("Technotronz'23 General Registration ")

name=st.text_input('Enter your full name:')
rollno=st.text_input('Enter your roll number: ')
mail=st.text_input('Enter your mail ID: ')
clg=st.text_input('Enter your college name: ')
year=st.selectbox("Year of study: ",options=["--Choose--","I","II","III","IV","V"],index=0)
ph=st.text_input('Your mobile number (follow this format - without country code: 935xxxxxxx): ')

def check(email):
            if not (re.fullmatch(regex, email)):
                        return 1
            return 0
def valid(name):
    name=name.replace(" ","").replace(".","")
    return name.isalpha()
def valid2(name):
    return name.replace(" ","").isalpha()

col1,col2,col3=st.columns([2,1,2])
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 255, 255);
    height:1.5em;
    width: 3em; 
    font-size: 29px;
    color: black;
}
</style>""", unsafe_allow_html=True)
with col2:
            d=st.button("Submit")
if d:
#   with col1:
        name_err=rollno_err=mail_err=clg_err=year_err=ph_err=pdf_err=0
        row=[name,rollno,mail,clg,year,ph]
        if not valid(name):
            st.error("Enter valid Name of participant")
        else:
            name_err=1
    ###
        if rollno=="" or rollno==' ':
            st.error("Enter valid Roll Number of participant")            
        else:
            rollno_err=1
    ###     
        if check(mail):
            st.error("Enter valid Mail ID of participant")
        else:
            mail_err=1
    ###
        if not valid2(clg):
            st.error("Enter valid College Name of participant")
        else:
            clg_err=1
    ###
        if year=="--Choose--":
            st.error("Enter year of study for participant")
        else:
            year_err=1
    ###
        if ph=="" or ph==' ' or not (ph[4:].isdigit()) or len(ph)<10 or len(ph)>10:
            st.error("Enter valid paricipant phone number")
        else:
            ph_err=1

    
        if name_err==rollno_err==mail_err==clg_err==year_err==ph_err==1:
            print(row)
            data=sheet.get_all_values()
            r=sheet.cell(len(data),1).value
            st.success("Your Registration ID is generated! Check your registered mail ID.")
            sheet.insert_row(["TZ23"+str(int(r[4:])+1)]+row,len(data)+1)
            C1,C2,C3,C4=st.columns([0.2,0.5,0.1,0.1])
            with C2:
                        note_gr = 'Got your registration ID? [Click here](https://technotronz-event-registration-cszffj.streamlit.app/) to register for events.'
                        st.markdown(note_gr, unsafe_allow_html=True)

