from elasticsearch import Elasticsearch, NotFoundError
import numpy as np

# Initialize the Elasticsearch client
# es = Elasticsearch(["http://localhost:9200"])  # Update with your Elasticsearch server details

# Define the index name
index_name = "job_search"

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "company": {"type": "keyword"},
            "salary": {"type": "text"},
            "city": {"type": "text"},
            "experience": {"type": "text"},
            "description": {"type": "text"},
            "requirements": {"type": "text"},
            "benefits": {"type": "text"},
            "location": {"type": "text"},
            "link": {"type": "text"},
            "deadline": {"type": "date"},
            "embedding": {"type": "dense_vector", "dims": 768}  # Adjust dims based on your model
        }
    }
}

# Function to create the index if it does not exist
def create_index(es):
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, body=index_settings)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index: {e}")

# Function to generate an embedding (dummy function for demonstration)
def generate_embedding(text):
    # Replace with actual embedding generation logic (e.g., using a model)
    # Here we generate a random embedding as a placeholder
    return np.random.rand(768).tolist()  # Adjust dimensions accordingly

# Function to add a job posting with embeddings
def add_job(es,job):
    # embedding = generate_embedding(description)  # Generate embedding from description
    job_doc = {
        "title": job["title"],
        "company": job["company"],
        "location": job["location"],
        "description": job["description"],
        "posted_date": job["deadline"],
        "embedding": generate_embedding(job["description"]),
        "requirements": job["requirements"]
    }
    try:
        es.index(index=index_name, document=job_doc)
        print(f"Job added: {title} at {company}")
    except Exception as e:
        print(f"Error adding job: {e}")

def search_jobs_by_embedding(input_embedding, top_k=5):
    # Normalize the input embedding
    input_embedding = np.array(input_embedding).tolist()  # Ensure it is a list

    # Construct the search query using cosine similarity
    query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.input_vector, doc['embedding']) + 1.0",
                    "params": {
                        "input_vector": input_embedding
                    }
                }
            }
        }
    }

    try:
        response = es.search(index=index_name, body=query)
        return response['hits']['hits']  # Return the top K results
    except Exception as e:
        print(f"Error searching for jobs: {e}")
        return []

# if __name__ == "__main__":
#     es = Elasticsearch(["http://localhost:9200"]) 
#     create_index(es)
#     es.close()
#     # Create the index if it doesn't exist
#     create_index()

#     # Add a job posting example
#     add_job(
#         title="Software Engineer",
#         company="Tech Corp",
#         location="New York, NY",
#         description="Develop and maintain software applications.",
#         posted_date="2024-10-01"
#     )
