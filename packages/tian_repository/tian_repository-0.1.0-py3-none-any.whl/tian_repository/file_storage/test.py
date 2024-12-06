import os
import pickle
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Step 1: Define the scope and authenticate
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(
        'client_secrets.json')
    # creds = flow.run_local_server(port=0)

    return creds

# Step 2: Connect to Google Sheets and Read/Write Data
def access_google_sheet(sheet_id, range_name):
    creds = authenticate_google_sheets()

    # Connect to the Google Sheets API
    service = build('sheets', 'v4', credentials=creds)

    # Access the sheet by ID and range
    sheet = service.spreadsheets()

    # Step 3: Read Data
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Data from the sheet:')
        for row in values:
            print(row)

    # Step 4: Writing Data (optional)
    # Example: Writing data to the sheet
    write_values = [
        ['A', 'B', 'C'],
        ['1', '2', '3'],
        ['4', '5', '6'],
    ]

    body = {
        'values': write_values
    }
    result = sheet.values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")



if __name__ == '__main__':
    # Replace with your Google Sheet ID and range
    SHEET_ID = '1-jQrFC_DD0iSvvDvLV8y21TJ-Q7uzpGC4f8JZYR9_ME'
    RANGE_NAME = 'Sheet1!A1:D10'
    access_google_sheet(SHEET_ID, RANGE_NAME)
