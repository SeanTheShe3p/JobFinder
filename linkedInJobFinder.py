import requests
import json
import docx2txt
from openai import OpenAI
import numpy as np
from scipy import spatial
import os

resume = "future_resume.docx"

api_url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
headers = {"x-rapidapi-key": "f9b97b91e1msh2ad180ecfa3bda4p1f548bjsnf087670dcd81","x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"}
keys_to_keep = ['date_validthrough','title','url','external_apply_url','description_text', 'employment_type','salary_raw', 'seniority', 'linkedin_org_description', 'external_apply_url']
resume = "futureresume.docx"
api = os.environ.get('OPENAI_API_KEY')
client = OpenAI(
    api_key = api,
)

def pull_api_data(url, headers, jobs):
    try:
        job_offers = ["" for j in range(jobs)]
        querystring = {"limit":jobs,"offset":0,"order":"asc","title_filter":"\"Android Developer\"","seniority":"Entry Level","location_filter":"\"United States\" OR \"United Kingdom\"","description_type":"text","type_filter":"FULL_TIME"}
        
        with requests.get(url, headers=headers, params=querystring) as response:
            if response.status_code == 200:
                data = json.loads(response.text)
                # print(data)
                for l in range(jobs):
                    for ele in keys_to_keep:
                        text = str(data[l][ele])
                        job_offers[l] += text
            return job_offers

    except requests.exceptions.RequestException as e:
        print("Error downloading", e)

def read_resume(filename):
    doc = docx2txt.process(filename)
    doc = doc.replace("\n", " ")
    return doc

def embedding_from_string(string,  model = "text-embedding-3-small"):
    response = client.embeddings.create(input=string, model="text-embedding-3-small").data
    return response

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def distances_from_embeddings(
    query_embedding: list[float],
    embeddings: list[list[float]],
    distance_metric="cosine",
) -> list[list]:
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    return np.argsort(distances)


def compare_data(job_offers, resume, model = "text-embedding-3-small") -> list[int]:
    job_offers.insert(0, resume)
    embeddings = [get_embedding(string, model=model) for string in job_offers]
    query_embedding = embeddings[0]
    
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
    
    return indices_of_nearest_neighbors

    

if __name__ == "__main__":
    resume = read_resume(resume)
    job_list = pull_api_data(api_url, headers, 10)
    top_jobs = compare_data(job_list, resume)

    with open("linkedIn.txt", 'at', encoding="utf-8") as f:
        for job in top_jobs:
            text = job_list[job].replace("\n", " ")
            f.write(text)
            f.write("\n")