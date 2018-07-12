# Builtins
import logging
from pprint import pprint

# Third Party
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_cors import CORS

logger = logging.getLogger(__name__)
app = Flask(
    __name__,
    static_folder="./dist/static",
    template_folder="./dist"
)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

people = {
    'akilah': {'name': 'akilah', 'full_name': 'Akilah', 'is_therapist': False},
    'robyn': {'name': 'robyn', 'full_name': 'Robyn', 'is_therapist': False},
    'timothy': {'name': 'timothy', 'full_name': 'Timothy', 'is_therapist': False},
    'deb': {'name': 'deb', 'full_name': 'Deb', 'is_therapist': True},
    'jennifer': {'name': 'jennifer', 'full_name': 'Jennifer', 'is_therapist': True},
    'april': {'name': 'april', 'full_name': 'April', 'is_therapist': True},
}

threads = {
    'akilah': [
        [
            {'sender': 'deb', 'message': 'S1 T1'},
            {'sender': 'akilah', 'message': 'S1 A1'},
            {'sender': 'akilah', 'message': 'S1 A2'},
            {'sender': 'deb', 'message': 'S1 T2'},
            {'sender': 'deb', 'message': 'S1 T3'},
            {'sender': 'deb', 'message': 'S1 T4'},
        ],
        [
            {'sender': 'deb', 'message': 'S2 T1'},
            {'sender': 'akilah', 'message': 'S2 A1'},
            {'sender': 'deb', 'message': 'S2 T2'},
        ]
    ],
    'robyn': [
        [
            {'sender': 'jennifer', 'message': 'S1 T1'},
            {'sender': 'robyn', 'message': 'S1 Robyn1'},
            {'sender': 'robyn', 'message': 'S1 Robyn2'},
            {'sender': 'jennifer', 'message': 'S1 T2'},
            {'sender': 'jennifer', 'message': 'S1 T3'},
            {'sender': 'jennifer', 'message': 'S1 T4'},
        ],
        [
            {'sender': 'jennifer', 'message': 'S2 T1'},
            {'sender': 'robyn', 'message': 'S2 Robyn1'},
            {'sender': 'jennifer', 'message': 'S2 T2'},
        ],
        [
            {'sender': 'jennifer', 'message': 'S3 T1'},
            {'sender': 'robyn', 'message': 'S3 Robyn1'},
            {'sender': 'robyn', 'message': 'S3 Robyn2'},
            {'sender': 'jennifer', 'message': 'S3 T2'},
            {'sender': 'robyn', 'message': 'S3 Robyn3'},
            {'sender': 'jennifer', 'message': 'S3 T3'},
            {'sender': 'robyn', 'message': 'S3 Robyn4'},
        ],
    ],
    'timothy': [
        [
            {'sender': 'april', 'message': 'S1 T1'},
            {'sender': 'timothy', 'message': 'S1 Tim1'},
            {'sender': 'timothy', 'message': 'S1 Tim2'},
            {'sender': 'april', 'message': 'S1 T2'},
            {'sender': 'april', 'message': 'S1 T3'},
            {'sender': 'april', 'message': 'S1 T4'},
        ],
        [
            {'sender': 'april', 'message': 'S2 T1'},
            {'sender': 'timothy', 'message': 'S2 Tim1'},
            {'sender': 'april', 'message': 'S2 T2'},
        ],
        [
            {'sender': 'april', 'message': 'S3 T1'},
            {'sender': 'timothy', 'message': 'S3 Tim1'},
            {'sender': 'timothy', 'message': 'S3 Tim2'},
            {'sender': 'april', 'message': 'S3 T2'},
            {'sender': 'timothy', 'message': 'S3 Tim1'},
        ],
    ],
}

@app.route('/api/people', methods=['GET'])
def get_people():
    try: 
        return make_response(jsonify(people))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

@app.route('/api/thread/<string:person>', methods=['GET'])
def get_thread(person):
    try: 
        thread_messages = threads[person]
        return make_response(jsonify(thread_messages))
    except Exception:
        logger.exception('500 Error Fetching Thread Data')
        abort(500)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
