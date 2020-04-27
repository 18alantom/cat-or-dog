import torch
from flask import render_template, request
from flask_server import app
from flask_server import classifier


@app.route("/")
def index():
    return render_template("index.html", flask_token="hurrah~! it works~!")


@app.route("/", methods=['POST'])
def get_verdict():
    data = request.get_data()
    verdict = classifier.classify(data)
    return verdict
