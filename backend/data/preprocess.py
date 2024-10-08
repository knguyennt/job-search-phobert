import json
from bs4 import BeautifulSoup
import pandas as pd


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Preprocess function
def preprocess_data(data):
    processed_jobs = []
    
    for job in data:
        processed_job = {
            "title": job["title"].strip().lower(),
            "company": job["company"].strip().lower(),
            "salary": job["salary"].strip().lower() if job["salary"] != "Thoả thuận" else "negotiable",
            "city": job["city"].strip().lower(),
            "experience": job["experience"].strip().lower(),
            "description": " ".join([BeautifulSoup(desc, "html.parser").get_text().strip().lower() for desc in job["description"]]).strip(),
            "requirements": " ".join([BeautifulSoup(req, "html.parser").get_text().strip().lower() for req in job["requirement"]]).strip() if job["requirement"] else "not provided",
            "benefits": " ".join([BeautifulSoup(ben, "html.parser").get_text().strip().lower() for ben in job["benefit"]]).strip() if job["benefit"] else "not provided",
            "location": job["location"].split(": ")[1].strip().lower() if ":" in job["location"] else job["location"].strip().lower(),
            "link": job["link"].strip().lower(),
            "deadline": job["deadline"].strip().split(": ")[1].lower() if ":" in job["deadline"] else "not provided"
        }
        processed_jobs.append(processed_job)
    
    return pd.DataFrame(processed_jobs)

# Run preprocessing
data = read_json_file('test.json')
df = preprocess_data(data)

# Check the preprocessed DataFrame
df.to_csv("data1.csv", index=False)
