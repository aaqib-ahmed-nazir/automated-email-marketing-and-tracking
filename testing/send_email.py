import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import uuid
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TRACKING_SERVER_URL = "https://cae8-182-180-11-96.ngrok-free.app"

SHEET_ID = "1mENt_MVX-e6ZxlsZhhzHQR1XxAdntXAVdWbUoDRtoNE"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

email_accounts = [
    {"email": os.getenv(f"EMAIL_{i}"), "password": os.getenv(f"PASSWORD_{i}")}
    for i in range(1, 7)  # Adjust range based on the number of accounts
    if os.getenv(f"EMAIL_{i}") and os.getenv(f"PASSWORD_{i}")
]

if not email_accounts:
    raise ValueError("No email accounts found in the .env file!")

EMAIL_SUBJECT = "Important Message for You"

PIXEL_IMAGE_PATH = 'pixel.png'

TRACKING_PIXEL_POSITION = 'header'  

def get_email_data_from_google_sheet():
    """
    Fetches email data from a public Google Sheet in CSV format.
    """
    try:
        data = pd.read_csv(SHEET_URL)
        return data
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return pd.DataFrame()

def generate_tracking_url(tracking_id):
    """
    Generates a tracking URL with the specified tracking ID, including 'pixel.png' in the path.
    """
    return f"{TRACKING_SERVER_URL}/pixel.png/{tracking_id}"

def embed_tracking_pixel(html_content, tracking_pixel, position='footer'):
    """
    Embeds the tracking pixel into the HTML content at the specified position.
    
    Parameters:
    - html_content (str): The original HTML content of the email.
    - tracking_pixel (str): The HTML <img> tag for the tracking pixel.
    - position (str): 'header' or 'footer' to specify where to embed the pixel.
    
    Returns:
    - str: The modified HTML content with the tracking pixel embedded and line breaks preserved.
    """
    html_content = html_content.replace('\n', '<br>')
    
    if position.lower() == 'header':
        return f"{tracking_pixel}<br>{html_content}"
    else:
        return f"{html_content}<br>{tracking_pixel}"


def send_emails(start_row, number_of_sends):
    """
    Sends emails with embedded tracking pixels.

    Parameters:
    - start_row (int): The starting row in the Google Sheet.
    - number_of_sends (int): The number of emails to send.
    """
    data = get_email_data_from_google_sheet()
    if data.empty:
        print("No data available to process. Exiting...")
        return

    sent_emails = set()

    for i in range(start_row, start_row + number_of_sends):
        if i >= len(data):
            break

        row = data.iloc[i]
        first_name = row.get('First Name', 'Valued Customer')
        last_name = row.get('Last Name', '')
        email_address = row.get('Email')
        email_body = row.get('Email Content')

        if pd.notna(email_address) and pd.notna(email_body):
            if email_address in sent_emails:
                print(f"Skipping {email_address}: Already sent.")
                continue

            try:
                tracking_id = str(uuid.uuid4())

                tracking_url = generate_tracking_url(tracking_id)

                tracking_pixel = f'<img src="{tracking_url}" alt="" width="1" height="1" style="display:none;">'

                # Convert email_body line breaks for HTML
                modified_html_body = embed_tracking_pixel(email_body, tracking_pixel, position=TRACKING_PIXEL_POSITION)

                account = random.choice(email_accounts)
                sender_email = account["email"]
                app_password = account["password"]

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.set_debuglevel(1)  
                server.ehlo()
                server.starttls()
                server.login(sender_email, app_password)

                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = email_address
                msg['Subject'] = EMAIL_SUBJECT

                text = email_body

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(modified_html_body, 'html')
                msg.attach(part1)
                msg.attach(part2)

                server.sendmail(sender_email, email_address, msg.as_string())
                server.quit()

                print(f"Email sent to {email_address} from {sender_email} ({first_name} {last_name}) with Tracking URL: {tracking_url}")
                sent_emails.add(email_address)

            except Exception as e:
                print(f"Failed to send email to {email_address}: {str(e)}")

        else:
            print(f"Skipping row {i}: Missing data")


if __name__ == "__main__":
    send_emails(start_row=0, number_of_sends=5)
