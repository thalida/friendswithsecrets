import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)

spreadsheet = gc.open_by_key('1NSAQQVHvUYSXV3WuXj47qwNOLwWfdONEO2va9JGFayY')
session_sheet = spreadsheet.get_worksheet(1)
session_data = session_sheet.get_all_values()
# print(session_sheet, session_data)
# print(worksheets, session1)
