import streamlit as st

from streamlit_supabase_auth import login_form, logout_button
from supabase import create_client
from loguru import logger 
import jwt
import requests
import json
import os

def main():
    ######<SUPABASE OAUTH>#####
    # Retrieve these values from your Supabase project settings
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    # SUPABASE_SERVICE_KEY = st.secrets['SUPABASE_SERVICE_KEY']

    # Set up the Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    session = login_form(
        url=SUPABASE_URL,
        apiKey=SUPABASE_ANON_KEY,
        providers=["apple", "facebook", "github", "google"],
        )

    # Display welcome message and user details
    if session:
        user_name=session['user']['user_metadata'].get('name')
        avatar_url = session['user']['user_metadata'].get('avatar_url')
        email_verified = session['user']['user_metadata'].get('email_verified')
        if not email_verified:
            st.error("Please use a verified email address to log in.")
        else:
            # Additional logic for when the user is authenticated...
            st.write(f"Welcome to QuestChat {user_name}!")
            with st.sidebar:
                    if user_name:  # Checking if user_name exists before attempting to display it
                        st.write(f"Welcome {user_name}!")
                    if avatar_url:  # Similarly, check for avatar_url
                        st.image(avatar_url, width=100)
                    logout_button(url=SUPABASE_URL, apiKey=SUPABASE_ANON_KEY)
    ######</SUPABASE OAUTH>#####
                    
            logger.debug(f"st.session_state Check_4_GLOBAL: {st.session_state}") # For Debugging LOGIN in session state
            
            # Get Double check user's data from Supabase
            logger.info(f" current session user: {supabase.auth.get_user(session['access_token'])}")
            decoded_token = jwt.decode(session['access_token'], options={"verify_signature": False})
            logger.info(f"Decoded JWT: {decoded_token}")

    ###<SUPABASE DATA INSERTION>###
            def make_supabase_request(method, url, headers, data=None):
                """Perform an HTTP request to Supabase."""
                if method.lower() == 'post':
                    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
                elif method.lower() == 'get':
                    response = requests.get(url, headers=headers, timeout=10)
                # Add other methods as needed
                response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
                return response

            def insert_or_update_user_data(table_name: str, user_data: dict):
                # Headers for the request
                headers = {
                    'Authorization': f'Bearer {session["access_token"]}',
                    'Content-Type': 'application/json',
                    'apikey': SUPABASE_ANON_KEY
                }

                # The URL to your Supabase table endpoint
                url = f'{SUPABASE_URL}/rest/v1/{table_name}'

                return make_supabase_request('post', url, headers, user_data)


            # Prepare the data for Supabase
            supabase_data = {
                "name": user_name,
                # "user_id": session['user'].get('id'),
                "email": session['user']['user_metadata'].get('email'),
                "picture_url": avatar_url
            }
            with st.sidebar:
                if st.button(label="insert data"):
                    try:
                        post_response = insert_or_update_user_data(
                            table_name="chat_history",
                            user_data=supabase_data
                        )

                        logger.info(f"Supabase Response: {post_response.status_code}")
                        
                        # Check if the request was successful
                        if post_response.status_code == 201:
                            st.success("User information added successfully to Supabase.")
                        else:
                            logger.error(f"Error inserting/updating user data: {response.text}")
                            st.error(f"There was an issue adding your information to Supabase: {response.text}")
                    except Exception as e:
                        logger.error(f"Exception occurred: {e}")
                        st.error(f"An exception occurred: {e}")
###</SUPABASE DATA INSERTION>###


if __name__ == "__main__":
    main()
