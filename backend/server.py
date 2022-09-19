from typing import List, Dict
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

 # Allow Cross-Origin Resource Sharing
CORS(app)

@app.route('/getData')
def get_data() -> List[Dict]:
    return [
        {
            'time': '19/09/2022 16:32:32',
            'nDevices': 0
        },
        {
            'time': '19/09/2022 16:37:32',
            'nDevices': 5
        },
        {
            'time': '19/09/2022 16:42:32',
            'nDevices': 9
        }
    ]

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()