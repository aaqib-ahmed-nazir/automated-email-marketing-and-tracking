import csv
import requests

# Google Apps Script Web App URL to trigger the email open status update
SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec'

# Function to update email status in the Google Sheet based on Tracking ID
def update_email_status(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV
        for row in reader:
            tracking_id = row['Tracking ID']
            opened = row['Opened']

            # If the email is opened (as indicated by the "Opened" column being "Yes")
            if opened == "Yes":
                print(f"Tracking ID {tracking_id} has been opened.")

                # Make a GET request to the Google Apps Script Web App to mark email as opened
                data = {
                    'trackingId': tracking_id  # Include the Tracking ID to update status in Google Sheet
                }

                try:
                    response = requests.get(SCRIPT_URL, params=data)  # Send a GET request to update the status
                    response.raise_for_status()  # Raise an exception if the response code is 4xx/5xx
                    print(f"Status of email with Tracking ID {tracking_id} has been updated.")
                    print(f"Response Status: {response.status_code}")
                    print(f"Response Text: {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Error updating status for Tracking ID {tracking_id}: {e}")

# Call the function
update_email_status('emails_status.csv')  # Path to your CSV with email and status details