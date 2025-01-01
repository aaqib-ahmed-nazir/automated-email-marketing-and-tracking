import csv
import requests
import uuid

# Google Apps Script Web App URL
SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec'

# Function to send emails using the Apps Script
def send_emails_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through the rows
        for row in reader:
            first_name = row['First Name']
            last_name = row['Last Name']
            email = row['Email']
            subject = row['Email Content'].split("\n")[0]  # First line as subject
            body = row['Email Content']  # Full email content

            # Generate a unique tracking ID for each email
            trackingId = str(uuid.uuid4())  # Or use random string method

            # Data to send to the Apps Script
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'subject': subject,
                'body': body,
                'trackingId': trackingId  # Include the generated trackingId
            }

            # Debug print statement to check if trackingId is being sent
            print(f"Sending email to {email} with trackingId {trackingId}")

            # Send a POST request to the Apps Script
            try:
                response = requests.post(SCRIPT_URL, data=data)
                response.raise_for_status()  # Raise an exception if the response code is 4xx/5xx
                print(f"Email sent to {email} successfully.")
                print(f"Response Status: {response.status_code}")
                print(f"Response Text: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending email to {email}: {e}")

# Call the function
send_emails_from_csv('mails3.csv')