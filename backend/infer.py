import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer

def infer_result(query, phobert, tokenizer):
    def encode_text(text):
        inputs = tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        with torch.no_grad():
            outputs = phobert(**inputs)
        return outputs.last_hidden_state.mean(dim=1)  # Get the mean of the hidden states


    def encode_job(job):
        combined_text = f"{job['title']} {job['location']} {job['salary']} {job['company']} {job['description']}"
        return encode_text(combined_text[:512])


    def find_top_matches(user_query, job_list, top_n=10):
        query_vector = encode_text(user_query)
        job_vectors = [encode_job(job) for job in job_list]

        similarities = cosine_similarity(query_vector, torch.vstack(job_vectors))

        # Get the top N matches
        top_indices = similarities[0].argsort()[-top_n:][::-1]

        return [job_list[i] for i in top_indices]


    # Read job listings from CSV
    job_list_df = pd.read_csv("./data/data2.csv")  # Ensure the CSV has appropriate columns
    job_list = job_list_df.to_dict(orient="records")

    # Find the top job matches
    top_jobs = find_top_matches(query, job_list, top_n=10)

    return top_jobs
