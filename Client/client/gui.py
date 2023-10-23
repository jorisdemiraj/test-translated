
import streamlit as st
from pathlib import Path
import base64
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from config.load_settings import APP_NAME, APP_PORT


# config info for the front end
st.set_page_config(
     page_title='Simple GUI for the task',
     layout="wide",

)

# convert the image to bytes
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# this is just a basic front end , nothng to see here, move along
def main():
    
    URL_PATH='http://'+APP_NAME+':'+ APP_PORT+'/'
    st.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' height=320>](https://streamlit.io/)'''.format(img_to_bytes("static/images/logomark_website.png")), unsafe_allow_html=True)

    col1v, col2v, col3v = st.columns(3)
    with col1v:
        button1 = st.button('Shorten URL')
    with col2v:
        button2 = st.button('Retrieve Original URL')
    with col3v:
        button3 = st.button('Statistics')
        
    if 'button1' not in st.session_state:
            st.session_state['button1'] = button1    
    if 'button2' not in st.session_state:
            st.session_state['button2'] = button2
    if 'button3' not in st.session_state:
            st.session_state['button3'] = button3  

    if button1:
            st.session_state['button1'] = True
            st.session_state['button2'] = False
            st.session_state['button3'] = False
    elif button2:
            st.session_state['button1'] = False
            st.session_state['button2'] = True
            st.session_state['button3'] = False
    elif button3:
            st.session_state['button1'] = False
            st.session_state['button2'] = False
            st.session_state['button3'] = True

    if st.session_state['button1']:
        print(st.session_state)

        if 'field1' not in st.session_state:
            st.session_state['field1'] = ''
        if 'field2' not in st.session_state:
            st.session_state['field2'] = ''

        field1 = st.text_input("Enter the URL to shorten", value=st.session_state['field1'])
        field2 = st.text_input("Enter your email", value=st.session_state['field2'])
        
        st.session_state['field1'] = field1
        
        st.session_state['field2'] = field2


        if st.button('Shorten the URL'):
            print("button")

            url = URL_PATH+'short_url'
            data = {'url': field1, 'email': field2}


            response = requests.post(url, data=data)
            parsed_response= json.loads(response.content)

            st.write('Status Code:', response.status_code)
            parsed_response= json.loads(response.content)
            st.write('Shortened URL:', parsed_response['Output']['short_url'])
            

    if st.session_state['button2']:
        print(st.session_state)

        if 'short_url' not in st.session_state:
            st.session_state['short_url'] = ''


        short_url = st.text_input("Enter short url to convert", value=st.session_state['short_url'])
        
        st.session_state['short_url'] = short_url
        


        if st.button('Retrieve URL'):
            print("button")

            url = URL_PATH+'original_url'
            data = {'url': short_url}


            response = requests.post(url, data=data)
            parsed_response= json.loads(response.content)

            st.write('Status Code:', response.status_code)
            if response.status_code!=200:
                st.write(parsed_response[0])
            else:
                parsed_response= json.loads(response.content)
                st.write('Original URL:', parsed_response['Output']['url'])

    if button3:

        url = URL_PATH+'statistics'
        print("test")
        response = requests.get(url)
        parsed_response= json.loads(response.content)
        print(parsed_response)
        emailsdf= parsed_response['Output']['email_stat']
        urldf= parsed_response['Output']['url_stat']

        try:
            dfemail = pd.DataFrame(emailsdf, index=[0])
            dfurl=pd.DataFrame(urldf, index=[0])
            dfemail.index = ['Total inserts']
            dfurl.index = ['Total asked']
            dfemail=dfemail.transpose()
            dfurl=dfurl.transpose()
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(dfemail)
            with col2:
                st.dataframe(dfurl)

            col1, col2 = st.columns(2)
            with col1:
                dfemail.plot(kind='bar')
                st.pyplot(plt)
            with col2:
                dfurl.plot(kind='bar')
                st.pyplot(plt)
        except:
            st.write('There is no data present.')


# run main()
if __name__ == '__main__':
    
    main()