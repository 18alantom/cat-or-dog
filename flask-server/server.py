import time
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return str(time.time())

