from flask import Flask, request
from train import train_job_embed
from infer import infer_result
from transformers import AutoModel, AutoTokenizer
from utils import read_json_file, preprocess_data, combine_job_string, encode_job
from elastic import create_index, add_job, search_jobs_by_embedding
from elasticsearch import Elasticsearch
import numpy as np
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

@app.route("/ai-core/insert-job") 
def insert_job():
    es = Elasticsearch(["http://es-container:9200"])
    try:
        create_index(es)

        data = read_json_file("./data/data.json")
        job_df = preprocess_data(data)

        for index, row in job_df.iterrows():
            job_object = {
                "title": row['title'],
                "company": row['company'],
                "salary": row['salary'],
                "city": row['city'],
                "experience": row['experience'],
                "description": row['description'],
                "requirements": row['requirements'],
                "benefits": row['benefits'],
                "location": row['location'],
                "link": row['link'],
                "deadline": row['deadline']
            }
            job_text = combine_job_string(job_object)
            job_embed = encode_job(phobert, tokenizer, job_text[:512])
            job_object["embedding"] = job_embed

            add_job(es, job_object)

        return "Embed success"
    except:
        return "Embed error"
    finally:
        es.close()



@app.route("/ai-core/search-job")
def search_job():

    return "Search result"
