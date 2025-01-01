import csv
import requests
import uuid

SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec'

def send_emails_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            first_name = row['First Name']
            last_name = row['Last Name']
            email = row['Email']
            subject = row['Email Content'].split("\n")[0]
            body = row['Email Content']

            trackingId = str(uuid.uuid4())

            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'subject': subject,
                'body': body,
                'trackingId': trackingId
            }

            print(f"Sending email to {email} with trackingId {trackingId}")

            try:
                response = requests.post(SCRIPT_URL, json=data)
                response.raise_for_status()
                print(f"Email sent to {email} successfully.")
                print(f"Response Status: {response.status_code}")
                print(f"Response Text: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending email to {email}: {e}")

send_emails_from_csv('mails3.csv')
