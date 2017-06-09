from flask import Flask, request, redirect
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.model import BaseModelView
from datetime import datetime
import uuid
import os

app = Flask(__name__)

mongodb_uri = os.environ.get("PROD_MONGODB", "mongodb://localhost/ftrack")
secret_key = os.environ.get("PROD_SECRET_KEY", "#sup3r s3cr3t!")
track_url = os.environ.get("TRACK_URL", "http://127.0.0.1:5000/")

app.config["MONGODB_SETTINGS"] = {"host":mongodb_uri}
app.config['SECRET_KEY'] = secret_key

db = MongoEngine()
db.init_app(app)

def randid():
    return str(uuid.uuid4())[:8]

# Models
class App(db.Document):
    name = db.StringField()
    aid = db.StringField(default=randid())
    def __unicode__(self):
        return self.name

class Message(db.Document):
    description = db.StringField()
    app_id = db.ReferenceField(App)
    mid = db.StringField(default=randid())
    def __unicode__(self):
        return self.description

class Track(db.Document):
    ts = db.DateTimeField()
    xip = db.StringField()
    lip = db.StringField()
    rid = db.StringField()
    ua = db.StringField()
    params = db.DictField()
    aid = db.StringField()
    mid = db.StringField()

class MessageView(ModelView):
    column_filters = ('description', 'app_id')

class CMessageView(ModelView): 
    column_formatters = dict(uid=lambda v,c,m,p: track_url + str(m.app_id.aid) + '/' + str(m.mid))
    column_list = ('uid','description', 'app_id')

class TrackView(ModelView):
    column_filters = ('ts','aid','mid', 'xip', 'lip', 'rid', 'ua')

class AppView(ModelView):
    coulmn_filters = ('_id', 'name')
    form_excluded_columns = ['aid']


# Routes
@app.route('/',methods=['GET'])
def index():
    return redirect('/admin')


if __name__ == '__main__':
    admin = Admin(app, name='admin', template_mode='bootstrap3')
    admin.add_view(TrackView(Track))
    admin.add_view(AppView(App))
    #admin.add_view(MessageView(Message))
    admin.add_view(CMessageView(Message, name="ccc"))
    app.run(host='0.0.0.0', port=8000, debug=True)
