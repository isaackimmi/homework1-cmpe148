import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage


def send_email(creds):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('This is the message for Homework1.')

        message['To'] = 'isaacmmikim@gmail.com'
        message['From'] = 'isaacmmikim@gmail.com'
        message['Subject'] = 'Homework1'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


def main():
    CLIENT_FILE = 'client_secret.json'
    SCOPES = ['https://mail.google.com/']

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        message = send_email(creds)
        if message is None:
            print("Error sending the email.")
        else:
            print(message)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
