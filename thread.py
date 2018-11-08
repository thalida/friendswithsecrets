# Builtins
import datetime
import logging
from pprint import pprint

# Custom
import people
import spreadsheet

class Thread():
    STARTDAY = datetime.date(2018, 9, 3)
    NUM_SESSIONS_PER_DAY = 1;

    def __init__(self, google_client, person):
        super(Thread, self).__init__()
        self.gc = google_client
        self.person = person
        self.file = spreadsheet.get_file(self.gc, self.person)
        self.used_cached_session = False;
        self.total_sessions = 10;
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

        return session;

    def get_sessions(self):
        self.used_cached_session = False;
        now = datetime.date.today()
        time_since_start = now - self.STARTDAY

        num_available_sessions = spreadsheet.count_all_sessions(self.file)

        if num_available_sessions is None:
            self.used_cached_session = True
            num_available_sessions = len(self.sessions.keys())

        num_visible_sessions = self.NUM_SESSIONS_PER_DAY * (time_since_start.days + 1)

        if num_visible_sessions > num_available_sessions:
            num_visible_sessions = num_available_sessions

        num_hidden_sessions = self.total_sessions - num_visible_sessions

        sessions = [self.get_session(i) for i in range(num_visible_sessions)] + ([None] * num_hidden_sessions)
        return (sessions, self.used_cached_session)
