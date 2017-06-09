from flask import Flask, request
from flask_pymongo import PyMongo
from datetime import datetime
import os

app = Flask(__name__)
is_prod = os.environ.get('IS_HEROKU', None)
app.config["MONGO_URI"] = "mongodb://localhost/track"

if is_prod:
    app.config["MONGO_URI"] = os.environ.get("PROD_MONGODB")

mongo = PyMongo(app, config_prefix='MONGO')

# 1x1 Pixel.
img = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE\x00\x00\x00\xa7z=\xda\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00\x00\x00\nIDAT\x08\xd7c`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82'

# with open('1x1.png', 'rb') as fp:
# img = fp.read()

@app.route('/',methods=['GET'])
def index():
    return 'Not found', 200

@app.route('/<app_id>/<msg_id>', methods=['GET'])
def track(app_id, msg_id):
    ts = datetime.utcnow()
    data = dict()
    data['ts'] = ts
    data['aid'] = app_id
    data['mid'] = msg_id
    data['params'] = dict(request.args)
    data['lip'] = request.remote_addr
    data['xip'] = request.headers.get('X-Forwarded-For', '')
    data['rid'] = request.headers.get('X-Request-Id', '')
    data['ua'] = request.headers.get('User-Agent', '')
    mongo.db.track.insert(data)
    return img, 200, {'Content-Type': 'image/png'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)