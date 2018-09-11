# Builtins
import datetime
import logging
from pprint import pprint

# Custom
import people
import spreadsheet

class Thread():
    STARTDAY = datetime.date(2018, 9, 8)
    NUM_SESSIONS_PER_DAY = 1;
    PERSON_SESSION_HEADERS = {
        'akilah': [
            {'key': 0, 'title': 'Journey', 'image_url': '/static/images/session/7.jpeg'},
            {'key': 1, 'title': 'Recovery', 'image_url': '/static/images/session/8.jpeg'},
            {'key': 2, 'title': 'Happiness', 'image_url': '/static/images/session/1.jpeg'},
            {'key': 3, 'title': 'Love', 'image_url': '/static/images/session/3.jpeg'},
            {'key': 4, 'title': 'Friendship', 'image_url': '/static/images/session/5.jpeg'},
            {'key': 5, 'title': 'Acceptance', 'image_url': '/static/images/session/7.jpeg'},
        ],
        'robyn': [
            {'key': 0, 'title': 'Recovery', 'image_url': '/static/images/session/1.jpeg'},
            {'key': 1, 'title': 'Family', 'image_url': '/static/images/session/2.jpeg'},
            {'key': 2, 'title': 'Acceptance', 'image_url': '/static/images/session/3.jpeg'},
            {'key': 3, 'title': 'Friendship', 'image_url': '/static/images/session/4.jpeg'},
            {'key': 4, 'title': 'Health', 'image_url': '/static/images/session/5.jpeg'},
            {'key': 5, 'title': 'Love', 'image_url': '/static/images/session/6.jpeg'},
        ],
        'timothy': [
            {'key': 0, 'title': 'Family', 'image_url': '/static/images/session/6.jpeg'},
            {'key': 1, 'title': 'Health', 'image_url': '/static/images/session/4.jpeg'},
            {'key': 2, 'title': 'Recovery', 'image_url': '/static/images/session/1.jpeg'},
            {'key': 3, 'title': 'Journey', 'image_url': '/static/images/session/2.jpeg'},
            {'key': 4, 'title': 'Happiness', 'image_url': '/static/images/session/8.jpeg'},
            {'key': 5, 'title': 'Friendship', 'image_url': '/static/images/session/3.jpeg'},
        ],
    }

    def __init__(self, google_client, person):
        super(Thread, self).__init__()
        self.gc = google_client
        self.person = person
        self.file = spreadsheet.get_file(self.gc, self.person)
        self.used_cached_session = False;
        self.max_sesions = 10;
        self.sessions = {};

    def get_session(self, session_index=0):
        session = spreadsheet.get_session(self.file, session_index)
        if session is None:
            self.used_cached_session = True;
            session = self.sessions.get(session_index, None)
        elif len(session) > 0:
            self.sessions[session_index] = session;
        else:
            session = None;

        return self._tmp_format_session(session);

    def get_sessions(self):
        now = datetime.date.today()
        time_since_start = now - self.STARTDAY

        new_max_sesions = spreadsheet.count_all_sessions(self.file)
        self.max_sesions = new_max_sesions if new_max_sesions is not None else self.max_sesions;

        num_visible_sessions = self.NUM_SESSIONS_PER_DAY * time_since_start.days
        num_visible_sessions = self.max_sesions if num_visible_sessions > self.max_sesions else num_visible_sessions
        num_hidden_sessions = self.max_sesions - num_visible_sessions

        self.used_cached_session = False;
        sessions = [self.get_session(i) for i in range(num_visible_sessions)] + ([None] * num_hidden_sessions)
        return (sessions, self.used_cached_session)

    def get_session_headers(self, person):
        return self.PERSON_SESSION_HEADERS[person]

    def _tmp_format_session(self, session):
        try:
            return [{'sender': self._tmp_get_sender(m['sender']), 'message_text': m['message_text']} for m in session]
        except (TypeError):
            return None

    def _tmp_get_sender(self, orig_sender):
        if orig_sender in list(people.PARTICIPANTS.keys()):
            sender = self.person
        else:
            sender = people.PARTICIPANT_TO_THERAPIST[self.person]['name']

        return sender
