# Builtins
import logging
from pprint import pprint

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

app.config['BASIC_AUTH_USERNAME'] = app_secrets.AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = app_secrets.AUTH_PASSWORD

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
google_client = spreadsheet.create_gc()
basic_auth = BasicAuth(app)

def get_n_thread_sessions(person, num_sessions):
    thread = Thread(google_client, person)
    return thread.get_n_sessions(num_sessions)

@app.route('/api/thread/<string:person>', methods=['GET'])
def get_thread(person):
    try:
        res = {
            'sessions': get_n_thread_sessions(person, 10),
            'participant': people.PARTICIPANTS[person],
            'therapist': people.PARTICIPANT_TO_THERAPIST[person],
        }
        return make_response(jsonify(res))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@basic_auth.required
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
