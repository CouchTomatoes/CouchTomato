from flask import Flask
import argparse

def cmd_couchtomato():
    app = Flask(__name__)
    app.run(debug = True)