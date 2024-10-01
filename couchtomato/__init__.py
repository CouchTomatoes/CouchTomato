from couchtomato.core.logger import CPLog
from flask import Flask
# from flask.module import Module
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)
log = CPLog(__name__)


# web = Module(__name__, 'web')
# @web.route('/')
@app.route('/')
def index():
    return render_template('index.html')