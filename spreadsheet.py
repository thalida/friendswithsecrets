# Third Party
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Custom
import people

CREDS_SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

def create_gc():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', CREDS_SCOPE)
    gc = gspread.authorize(credentials)
    return gc

def get_file(gc, person):
    return gc.open_by_key(people.PERSON_TO_SHEET[person])

def count_all_sessions(file):
    try:
        return len(file.worksheets()) - 1
    except gspread.exceptions.APIError:
        return None;

def get_session(file, session_index):
    try:
        sheet = file.get_worksheet(session_index + 1)
    except gspread.exceptions.APIError:
        return None;

    try:
        session = sheet.get_all_values()
        return _format_session(session, sheet.title)
    except gspread.exceptions.APIError:
        return None;
    except AttributeError:
        return []

def _format_session(session, title=""):
    formatted_session = {
        'title': title.split(':', 1)[-1].strip(), 
        'messages': []
    }

    for field in session:
        txt = field[0]
        txt_lower = txt.lower()

        if len(txt) < 0:
            continue

        if txt_lower in list(people.PEOPLE.keys()):
            sender = txt_lower;
            continue
        elif txt_lower in list(people.PEOPLE_ALIAS_MAP.keys()):
            sender = people.PEOPLE_ALIAS_MAP[txt_lower];
            continue

        if sender:
            formatted_session['messages'].append({'sender': sender, 'message_text': txt});
            sender = None

    return formatted_session
