# Builtins
import logging
from pprint import pprint
import random

# Third Party
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_cors import CORS
from flask_basicauth import BasicAuth

# Custom
import app_secrets
import people
import spreadsheet
from thread import Thread

logger = logging.getLogger(__name__)
app = Flask(
    __name__,
    static_folder="./dist/static",
    template_folder="./dist"
)

# app.config['BASIC_AUTH_USERNAME'] = app_secrets.AUTH_USERNAME
# app.config['BASIC_AUTH_PASSWORD'] = app_secrets.AUTH_PASSWORD

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
google_client = spreadsheet.create_gc()
# basic_auth = BasicAuth(app)

threads = {};

def shuff(arr):
    try:
        random.shuffle(arr)
        return arr
    except (TypeError):
        return  arr

def get_thread_class(person):
    try:
        return threads[person]
    except (KeyError):
        threads[person] = Thread(google_client, person)
        return threads[person]

@app.route('/api/people', methods=['GET'])
def get_people():
    try:
        res = {
            'people': people.PEOPLE,
            'participantOrder': people.PARTICIPANT_ORDER,
        }
        return make_response(jsonify(res))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

@app.route('/api/thread/<string:person>', methods=['GET'])
def get_thread(person):
    try:
        thread = get_thread_class(person)
        (sessions, used_cached) = thread.get_sessions()

        res = {
            'sessions': sessions,
            'used_cached': used_cached,
            'participant': people.PARTICIPANTS[person],
            'therapist': people.PARTICIPANT_TO_THERAPIST[person],
        }
        return make_response(jsonify(res))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

# @basic_auth.required
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
