import requests
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import email_google_sheet
from create_email import create_email

# Constants for Zoho API
CLIENT_ID = "1000.EX3EA1HGIBN8NGIUH5LCN5T3DHOL3F"
CLIENT_SECRET = "8b5111a7a9f8faabdd5f131b18d7eb243eee98d675"
REFRESH_TOKEN = "1000.e8299e9c3692ee87a8aa84f30c1c4378.d44eee738e19d70be38bc9bb072682d0"
ZOHO_API_BASE_URL = "https://www.zohoapis.com/crm/v2"
TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"

# Constants for Google Sheets
SPREADSHEET_ID = email_google_sheet
SERVICE_ACCOUNT_FILE = '/home/fox/ai/src/credentials.json'

def get_access_token(client_id, client_secret, refresh_token):
    payload = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

def fetch_emails_from_zoho(access_token):
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    response = requests.get(f"{ZOHO_API_BASE_URL}/Leads", headers=headers)
    response.raise_for_status()
    return [record.get("Email") for record in response.json().get("data", []) if record.get("Email")]

def upload_to_google_sheets(data):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build('sheets', 'v4', credentials=credentials)
    
    values = [[row.get('Email_address'), row.get('Subject'), row.get('Email Template Body')] for row in data]
    
    body = {'values': values}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1', 
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS", 
        body=body
    ).execute()

def main():
    print("Authenticating with Zoho CRM...")
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    print("Fetching emails from Zoho CRM...")
    zoho_emails = fetch_emails_from_zoho(access_token)

    if not zoho_emails:
        print("No emails found!")
        return

    # Save Zoho emails to CSV file
    pd.DataFrame({"Email": zoho_emails}).to_csv("data/zoho_emails.csv", index=False)
    print(f"Saved {len(zoho_emails)} emails to data/zoho_emails.csv")

    # Generate emails based on `prospects.csv`
    generated_emails_df = create_email()
    email_data = generated_emails_df.to_dict('records')
    upload_to_google_sheets(email_data)

    print("Emails successfully uploaded to Google Sheets!")

if __name__ == "__main__":
    main()