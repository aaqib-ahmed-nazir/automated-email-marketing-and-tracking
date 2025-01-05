import gspread
from oauth2client.service_account import ServiceAccountCredentials
from create_call_script import generate_call_script
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

def process_email_tracking(sheet_id, new_sheet_id):
    """
    - Parameters:
        - sheet_id: str (The source Google Sheet containing email tracking data)
        - new_sheet_id: str (The destination Google Sheet where leads will be uploaded)

    - Returns:
        - None

    - Description:
        - This function processes all rows in the email tracking sheet where 'Open_Amount' > 5.
        - For each qualifying lead, it generates a call script and uploads the data to a new Google Sheet.
    """
    client = authorize_google_sheets()
    sheet = client.open_by_key(sheet_id).sheet1

    rows = sheet.get_all_records()

    for i in range(len(rows) - 1, -1, -1):  
        row = rows[i]
        email = row.get('Email_address')  
        try:
            open_amount = int(row.get('Open_Amount', 0))  
        except (ValueError, TypeError):
            open_amount = 0

        if open_amount > 5:
            # Generate call script
            call_script = generate_call_script(row)

            # Upload the lead to the specified Google Sheet
            upload_lead_to_endpoint(email, call_script, new_sheet_id)

            # Remove the processed row from the source sheet
            sheet.delete_rows(i + 2) 

            print(f"Processed and removed row for email: {email}")
    
    return None 


def upload_lead_to_endpoint(email, call_script, new_sheet_id):
    """
    - Parameters:
        - email: str
        - call_script: str
        - new_sheet_id: str

    - Returns:
        - None

    - Description:
        - This function uploads the email, first name, last name, and call script to a specified Google Sheet
          using its sheet ID.
    """

    client = authorize_google_sheets()
    
    try:
        sheet = client.open_by_key(new_sheet_id).sheet1
    except gspread.exceptions.APIError as e:
        print(f"Error accessing the sheet: {e}")
        return

    try:
        first_name, last_name = email.split('@')[0].split('.')
    except ValueError:
        first_name = email.split('@')[0]
        last_name = ""

    sheet.append_row([email, first_name, last_name, call_script])

    print(f"Lead successfully uploaded for: {email}")

if __name__ == "__main__":
    source_sheet_id = '16pUY4X33SWesKGWUrCTLJ7h7CteHOLqW9W1oxXv_vyw'  # Source sheet with email tracking
    destination_sheet_id = '1dUEOzz5gd10LcUZOYfuo3etQrNlyhp5mJQU4rDIBTIo'  # Destination sheet for processed leads

    process_email_tracking(source_sheet_id, destination_sheet_id)