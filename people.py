PEOPLE = {
    'akilah': {'name': 'akilah', 'full_name': 'Akilah', 'is_therapist': False},
    'robyn': {'name': 'robyn', 'full_name': 'Robyn', 'is_therapist': False},
    'timothy': {'name': 'timothy', 'full_name': 'Timothy', 'is_therapist': False},
    'deb': {'name': 'deb', 'full_name': 'Deb', 'is_therapist': True},
    'jennifer': {'name': 'jennifer', 'full_name': 'Jennifer', 'is_therapist': True},
    'laura': {'name': 'laura', 'full_name': 'Laura', 'is_therapist': True},
}

PEOPLE_ALIAS_MAP = {
    'tim': 'timothy'
}

PARTICIPANT_ORDER = ['akilah', 'robyn', 'timothy'];

PARTICIPANTS = {
    'akilah': PEOPLE['akilah'],
    'robyn': PEOPLE['robyn'],
    'timothy': PEOPLE['timothy'],
}

PARTICIPANT_TO_THERAPIST = {
    'akilah': PEOPLE['deb'],
    'robyn': PEOPLE['jennifer'],
    'timothy': PEOPLE['laura'],
}

PERSON_TO_SHEET = {
    'akilah': '1_HNjbW5DiYsDJNQ2Wvd3iphn2IImZu995PPERc1GIv4',
    'robyn': '1NSAQQVHvUYSXV3WuXj47qwNOLwWfdONEO2va9JGFayY',
    'timothy': '1iEFuNiykCe9_n1Y96Y_IsGQCiXho_wn-aVSsdGTZuc0',
}
