# Change the import order and things break.
from flask import Flask
app = Flask(__name__)

import flask_server.classifier as classifier
import flask_server.views
