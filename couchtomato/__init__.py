from couchtomato.core.auth import requires_auth
from couchtomato.core.logger import CPLog
from couchtomato.environment import Env
from flask import Flask, Blueprint
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.utils import redirect
import os

app = Flask(__name__)
log = CPLog(__name__)
web = Blueprint('web', __name__)
base = declarative_base()

def get_session(engine):
    engine = engine if engine else get_engine()
    return scoped_session(sessionmaker(autoflush = True, transactional = True, bind = engine))

def get_engine():
    return create_engine('sqlite:///' + Env.get('db_path'), echo = Env.get('debug'))
    

@web.route('/')
@requires_auth
@app.route('/')
def index():
    return render_template('index.html', sep = os.sep)

@app.errorhandler(404)
def page_not_found(error):
    index_url = url_for('web.index')
    url = request.path[len(index_url):]
    return redirect(index_url + '#' + url)