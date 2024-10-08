from flask import Flask, request
from train import train_job_embed
from infer import infer_result
from transformers import AutoModel, AutoTokenizer
from utils import read_json_file, preprocess_data
import sys

app = Flask(__name__)

try:
    model = "./phobert-finetuned"
    phobert = AutoModel.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model)
except:
    model = "vinai/phobert-base-v2"
    phobert = AutoModel.from_pretrained(model)
    tokenizer = AutoTokenizer.from_pretrained(model)


@app.route("/ai-core/train")
def train():
    data = read_json_file("./data/data.json")
    job_df = preprocess_data(data)
    train_job_embed()

    return "<p>Train complete</p>"


@app.route("/ai-core/infer", methods=['POST'])
def infer():
    json_data = request.get_json()
    result = infer_result(json_data["query"], phobert, tokenizer)
    return result
