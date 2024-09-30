import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer

# Load PhoBERT model and tokenizer
model = "./phobert-finetuned"
# model = "vinai/phobert-base-v2"
phobert = AutoModel.from_pretrained(model)
tokenizer = AutoTokenizer.from_pretrained(model)


def encode_text(text):
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=512
    )
    with torch.no_grad():
        outputs = phobert(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Get the mean of the hidden states


def encode_job(job):
    combined_text = f"{job['title']} {job['description']} {job['salary']} {job['company']} {job['location']}"
    return encode_text(combined_text)


def find_top_matches(user_query, job_list, top_n=10):
    query_vector = encode_text(user_query)
    job_vectors = [encode_job(job) for job in job_list]

    similarities = cosine_similarity(query_vector, torch.vstack(job_vectors))

    # Get the top N matches
    top_indices = similarities[0].argsort()[-top_n:][::-1]

    return [job_list[i] for i in top_indices]


# Read job listings from CSV
job_list_df = pd.read_csv("data.csv")  # Ensure the CSV has appropriate columns
job_list = job_list_df.to_dict(orient="records")

# User query
user_query = (
    "Tôi tìm kiếm công việc kỹ sư vue tại Hồ Chí Minh với mức lương 25 triệu."
)

# Find the top job matches
top_jobs = find_top_matches(user_query, job_list, top_n=10)

# Print the top job matches
print("Công việc phù hợp nhất:")
for job in top_jobs:
    print(job)
