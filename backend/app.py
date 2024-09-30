from flask import Flask, request
from train import train_job_embed
from infer import infer_result
from transformers import AutoModel, AutoTokenizer
import sys

app = Flask(__name__)

# Load PhoBERT model and tokenizer
try:
    model = "./phobert-finetuned"
    phobert = AutoModel.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model)
except:
    model = "vinai/phobert-base-v2"
    phobert = AutoModel.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ai-core/train")
def train():
    train_job_embed()

    return "<p>Train complete</p>"


@app.route("/ai-core/infer", methods=['POST'])
def infer():
    json_data = request.get_json()
    result = infer_result(json_data["query"], phobert, tokenizer)
    return result
