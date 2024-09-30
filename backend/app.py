from flask import Flask
from train import train_job_embed

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ai-core/train")
def train():
    train_job_embed()
    
    return "<p>Training</p>"