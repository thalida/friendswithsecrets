# Builtins
import logging
from pprint import pprint

# Custom
import people
import spreadsheet

class Thread():
    def __init__(self, google_client, person):
        super(Thread, self).__init__()
        self.gc = google_client
        self.person = person
        self.file = spreadsheet.get_file(self.gc, self.person)

    def get_session(self, session_index=0):
        session = spreadsheet.get_session(self.file, session_index)
        return self._tmp_format_session(session);

    def get_n_sessions(self, n):
        sessions = [self.get_session(i) for i in range(n)]
        return [session for session in sessions if session is not None ]

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
