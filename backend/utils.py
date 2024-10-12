import json
from bs4 import BeautifulSoup
import pandas as pd
import torch

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def preprocess_data(data):
    processed_jobs = []
    
    for job in data:
        if not isinstance(job, dict):  # Check if job is a valid dictionary
            continue  # Skip this iteration if it's not
        
        processed_job = {
            "title": job.get("title", "").strip().lower() if job.get("title") else "",
            "company": job.get("company", "").strip().lower() if job.get("company") else "",
            "salary": job.get("salary", "").strip().lower() if job.get("salary") != "Thoả thuận" else "negotiable",
            "city": job.get("city", "").strip().lower() if job.get("city") else "",
            "experience": job.get("experience", "").strip().lower() if job.get("experience") else "",
            "description": " ".join([
                BeautifulSoup(desc, "html.parser").get_text().strip().lower() 
                for desc in job.get("description", [])
            ]).strip(),
            "requirements": " ".join([
                BeautifulSoup(req, "html.parser").get_text().strip().lower() 
                for req in job.get("requirement", [])
            ]).strip() if job.get("requirement") else "not provided",
            "benefits": " ".join([
                BeautifulSoup(ben, "html.parser").get_text().strip().lower() 
                for ben in job.get("benefit", [])
            ]).strip() if job.get("benefit") else "not provided",
            "location": job.get("location", "").split(": ")[1].strip().lower() if ":" in job.get("location", "") else job.get("location", "").strip().lower(),
            "link": job.get("link", "").strip().lower() if job.get("link") else "",
            "deadline": job.get("deadline", "").strip().split(": ")[1].lower() if ":" in job.get("deadline", "") else "not provided"
        }
        processed_jobs.append(processed_job)

        pd.DataFrame(processed_jobs).to_csv("data2.csv", index=False)
    
    return pd.DataFrame(processed_jobs)


def combine_job_string(job):
    combined_text = f"{job['title']} {job['location']} {job['salary']}"
    return combined_text

def encode_job(model, tokenizer, job_text):
    inputs = tokenizer(
        job_text, return_tensors="pt", truncation=True, padding=True, max_length=512
    )
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def elastic_save_job(job, job_embedding):

    pass