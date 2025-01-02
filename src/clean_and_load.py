import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

def authorize_google_sheets():
    """
        - Parameters: 
            - None
            
        - Returns:
            - client: gspread client object
            
        - Description:
            - This function authorizes the Google Sheets API and returns a client
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    return client

def process_email_tracking(sheet_id):
    """
        - Parameters:
            - sheet_id: str
            
        - Returns:
            - None
            
        - Description:
            - This function processes the email tracking sheet and uploads leads to the endpoint
    """
    client = authorize_google_sheets()
    sheet = client.open_by_key(sheet_id).sheet1

    rows = sheet.get_all_records()

    for i in range(len(rows) - 1, -1, -1):
        row = rows[i]
        email = row['Email_address']
        try:
            open_amount = int(row['Open_Amount'])
        except (ValueError, TypeError):
            open_amount = 0

        if open_amount > 5:
            call_script = generate_call_script(row)

            upload_lead_to_endpoint(email, call_script)

            sheet.delete_rows(i + 2)

            print(f"Processed and removed row for email: {email}")

def generate_call_script(row):
    """
        Need to implement...
    """
    print("In call script")
    pass

def upload_lead_to_endpoint(email, call_script):
    pass 

if __name__ == "__main__":
    sheet_id = '14aOJaQ5SXAPs1rrLWgRrgUAnPk74dSMeMzt3iNkxMxg'  # test sheet id
    process_email_tracking(sheet_id)