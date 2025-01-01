import pandas as pd

# Fetch and analyze email tracking data from Google Sheet
def fetch_email_tracking_data(sheet_url):
    # Load the Google Sheet data into a Pandas DataFrame
    tracking_data = pd.read_csv(sheet_url)

    # Print the fetched data
    print("Fetched Data:")
    print(tracking_data.head())

    # Check for required columns
    print("Columns in the data:", tracking_data.columns)

    # Analyze open rates
    if 'Tracking ID' in tracking_data.columns and 'Status' in tracking_data.columns:
        open_rates = tracking_data.groupby('Tracking ID')['Status'].apply(lambda x: (x == 'OPENED').sum())
        print("Open Rates:")
        print(open_rates)
    else:
        print("Required columns ('Tracking ID', 'Status') are missing.")

# Call the function with your Google Sheet's "export as CSV" URL
fetch_email_tracking_data("https://docs.google.com/spreadsheets/d/1UFjMOQRLOAoUmJnoMCa9EbEhI7W5tfOnBPYYpGdUUN8/export?format=csv")