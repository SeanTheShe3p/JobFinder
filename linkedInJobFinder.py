import requests
import json
import docx2txt
from openai import OpenAI
import numpy as np
from scipy import spatial
import os

# Constants/headers
resume = "future_resume.docx"
api_url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
headers = {"x-rapidapi-key": "f9b97b91e1msh2ad180ecfa3bda4p1f548bjsnf087670dcd81","x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"}
keys_to_keep = ['date_validthrough','title','url','external_apply_url','description_text', 'employment_type','salary_raw', 'seniority', 'linkedin_org_description', 'external_apply_url']
resume = "resume.docx"
api = os.environ.get('OPENAI_API_KEY')
# Create an instance of the OpenAI client with API key in environment variables
client = OpenAI(
    api_key = api
)

# retrieve job postings from API
def pull_api_data(url, headers, jobs):
    try:
        job_offers = ["" for j in range(jobs)]
        # The actual search parameters
        querystring = {"limit":jobs,"offset":0,"order":"asc","title_filter":"\"Developer\"","description_filter":"Front End | Frontend","seniority":"Entry Level","location_filter":"\"United States\" OR \"United Kingdom\"","description_type":"text","type_filter":"FULL_TIME"}
        with requests.get(url, headers=headers, params=querystring) as response:
            if response.status_code == 200:
                data = json.loads(response.text)
                for l in range(jobs):
                    for ele in keys_to_keep:
                        # url requires a space before and after, so urls can be hyperlinked correctly
                        if ele == 'url':
                            job_offers[l]+= " "
                        text = str(data[l][ele])
                        job_offers[l] += text
                        if ele == 'url':
                            job_offers[l]+= " "
            return job_offers
    except requests.exceptions.RequestException as e:
        print("Error downloading", e)

# Read in resume, strip all newlines to make a single line string
def read_resume(filename):
    doc = docx2txt.process(filename)
    doc = doc.replace("\n", " ")
    return doc

# The function that is called to get an embedding from OpenAI
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

# This is the function that uses SciPy module spatial to calculate cosine similarity of given embedddings
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

# uses the array of distances to sort the list of embeddings based on their closest relatives
def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    return np.argsort(distances)

# the main OpenAi function, adds the resume to the joboffers array, gets all embeddings,
# calculates distances from embeddings and returns the order of similarity
def compare_data(job_offers, resume, model = "text-embedding-3-small") -> list[int]:
    job_offers.insert(0, resume)
    embeddings = [get_embedding(string, model=model) for string in job_offers]
    query_embedding = embeddings[0]
    
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
    
    return indices_of_nearest_neighbors

# main function call can edit number of jobs called, the top n items or the title of the output file.
if __name__ == "__main__":
    resume = read_resume(resume)
    job_list = pull_api_data(api_url, headers, 99)
    top_jobs = compare_data(job_list, resume)
    topTen = ["" for i in range(10)]
    with open("linkedIn.txt", 'at', encoding="utf-8") as f:  
        for m, job in enumerate(top_jobs[1:11]):
            topTen[m] = job_list[job].replace("\n", " ")
        for topjob in topTen:
            f.write(topjob) 
            f.write("\n")           