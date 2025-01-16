# Automated Email Marketing, Tracking, and Call Script Generation with Google Apps Script

## Flow Diagram
![System Flow Diagram](docs/diagram.png)

## Demo Video For Email Tracking
https://github.com/user-attachments/assets/74bcf609-1499-41e9-b3cb-a3f01ba4bc1a

## Repository Structure
```text
app_script_email_automation/
├── README.md
├── requirements.txt
└── src/
    ├── app_script.js                 (Main Apps Script code)
    ├── credentials.json              (Credentials for external services)
    ├── get_emails.py                 (Fetches and uploads email data to Sheets)
    ├── clean_and_gen_call_script.py  (Cleans data & triggers call script creation)
    └── functions/
        ├── agent.py                 (AI-related logic)
        ├── config.py                (Configuration & constants)
        ├── create_call_script.py    (Generates call scripts)
        ├── create_email.py          (Builds email content)
        └── utlis.py                 (Utility functions)
```

## Features
- Send emails from multiple aliases.
- Track opens with a web app and hidden pixel.
- Log open counts and timestamps in Google Sheets.
- Dynamically generate call scripts for emails exceeding five opens.
- Append generated scripts to a separate Sheet for follow-up actions.

## Getting Started
1. **Set Up Google Sheets**: Create or update source/destination Sheets for email list and lead data.  
2. **Deploy Web App**: Host the code in Google Apps Script and enable the web endpoint for open tracking.  
3. **Configure Credentials**: Store any required credentials for third-party services (e.g., OpenAI API).  
4. **Run & Track**: Send emails, check open stats, and watch new call scripts appear in the leads Sheet.

## Project Setup
1. **Clone the Repository**  
``` bash
https://github.com/aaqib-ahmed-nazir/automated-email-marketing-and-tracking.git
```
``` bash
   cd automated-email-marketing-and-tracking
```
2. **Create Environment File (.env)**  
   - Add your OpenAI API key and other credentials.  
   - Copy and paste the following into your `.env` file, replacing the placeholder values with your actual keys:

   ```env
   OPENAI_API_KEY=your_key_here
   SHEET_API_KEY=your_sheet_key_here
   ```

3. **Install Dependencies**  
   - In local Python projects, run:  
     pip install -r requirements.txt  

4. **Create or Update config.py**  
   Place this file under `src/helpers/` and store your credentials, Sheet IDs, and any other constants.  
   For example:

   ```python
   email_google_sheet = "YOUR_EMAIL_SHEET_ID"
   call_script_google_sheet = "YOUR_CALL_SCRIPT_SHEET_ID"
   CLIENT_ID = "YOUR_ZOHO_CLIENT_ID"
   CLIENT_SECRET = "YOUR_ZOHO_CLIENT_SECRET"
   REFRESH_TOKEN = "YOUR_ZOHO_REFRESH_TOKEN"
   ZOHO_API_BASE_URL = "https://www.zohoapis.com/crm/v2"
   TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
   ```

5. **Configure Google Apps Script**  
   - Paste the `.gs` / `app_script.js` code into your Google Apps Script Editor.  
   - Set up triggers or web app deployments as required.

6. **Deploy Production**  
   - Push your local changes to GitHub or your chosen repo host.  
   - In Google Apps Script, deploy with appropriate permissions for the tracking pixel.

## Setup and Usage
- Configure your [Google Apps Script](https://developers.google.com/apps-script) project with the provided code.
- Enable the web endpoint for handling the tracking pixel.
- Create or update your [Google Sheets](https://www.google.com/sheets/about/) for storing email data, tracking opens, and logging call scripts.
- Set necessary environment variables (e.g., API keys) in your script or use a .env file locally.
- Deploy as a web app; then run the main script to send emails and track opens.

## Additional Steps to Run
1. Activate your virtual environment (.venv) if needed, then run `get_emails.py` to gather and upload emails to a Google Sheet.
2. Open the Google Apps Script editor and run `app_script.js` via the web interface to handle sending and tracking.

## Workflow Overview (Step-by-Step)
1. **Data Import and Comparison**  
   - Import existing customers from Zoho CRM.  
   - Import new customer data from a CSV file.  
   - Compare the domains of existing and new customers.

2. **AI-Powered Email Generation**  
   - If a domain match is found, generate a personalized email using AI.  
   - Otherwise, generate a generic marketing email.

3. **Email Upload and Sending**  
   - Upload generated emails to a Google Sheet.  
   - Send all emails from the Sheet using Google Apps Script.

4. **Email Tracking**  
   - Track email activity via Google Apps Script.  
   - Update the Sheet with open status whenever an email is opened.

5. **Engagement Analysis and Call Script Generation**  
   - If an email’s open rate exceeds the threshold:  
     - Generate a personalized call script via AI.  
     - Save this call script to another Google Sheet for follow-up.

## Resources
- [Google Apps Script Overview](https://developers.google.com/apps-script)
- [Google Sheets](https://www.google.com/sheets/about/)
- [OpenAI GPT-4.0](https://openai.com/product/gpt-4)

## Contributors
This project was not possible without these amazing contributors:
- [Hashim Muhammad Nadeem](https://github.com/hash2004)
- [Haroon Wajid](https://github.com/haroonwajid)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
