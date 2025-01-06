# Email Automation using Google Apps Script & Call Script Generation

## Demo Video
https://github.com/user-attachments/assets/74bcf609-1499-41e9-b3cb-a3f01ba4bc1a

## Repository Structure
```text
app_script_email_automation/
├── README.md
└── src/
    ├── app_script.js
    ├── create_call_script.py
    └── clean_and_gen_call_script.py
```

## Features
- Send emails from multiple aliases.
- Track opens with a web app and hidden pixel.
- Log open counts and timestamps in Google Sheets.
- Dynamically generate call scripts for emails exceeding five opens.
- Append generated scripts to a separate Sheet for follow-up actions.

## How It Works
1. The web app pulls recipient info from a Sheet, iterates through multiple sender aliases, and sends emails.  
2. Each email includes a tracking pixel that logs opens and increments a counter.  
3. Upon reaching the open threshold, a GPT-4.0 request creates a short call script.  
4. The script is then appended to a designated Sheet for sales or marketing use.

## Getting Started
1. **Set Up Google Sheets**: Create or update source/destination Sheets for email list and lead data.  
2. **Deploy Web App**: Host the code in Google Apps Script and enable the web endpoint for open tracking.  
3. **Configure Credentials**: Store any required credentials for third-party services (e.g., OpenAI API).  
4. **Run & Track**: Send emails, check open stats, and watch new call scripts appear in the leads Sheet.

## Project Setup
1. **Clone the Repository**  
``` bash
https://github.com/aaqib-ahmed-nazir/email_automation_with_call_script_generation.git
```
``` bash
   cd app_script_email_automation
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

4. **Configure Google Apps Script**  
   - Paste the `.gs` / `app_script.js` code into your Google Apps Script Editor.  
   - Set up triggers or web app deployments as required.

5. **Deploy Production**  
   - Push your local changes to GitHub or your chosen repo host.  
   - In Google Apps Script, deploy with appropriate permissions for the tracking pixel.

## Setup and Usage
- Configure your [Google Apps Script](https://developers.google.com/apps-script) project with the provided code.
- Enable the web endpoint for handling the tracking pixel.
- Create or update your [Google Sheets](https://www.google.com/sheets/about/) for storing email data, tracking opens, and logging call scripts.
- Set necessary environment variables (e.g., API keys) in your script or use a .env file locally.
- Deploy as a web app; then run the main script to send emails and track opens.

## Resources
- [Google Apps Script Overview](https://developers.google.com/apps-script)
- [Google Sheets](https://www.google.com/sheets/about/)
- [OpenAI GPT-4.0](https://openai.com/product/gpt-4)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
