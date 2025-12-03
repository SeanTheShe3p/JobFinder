## refactored code



import requests
import json
import docx2txt
from openai import OpenAI
import numpy as np
from scipy import spatial
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# force reload the dotenv file
load_dotenv(override=True)

api_url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
headers = {"x-rapidapi-key": os.getenv('RAPID_API_KEY'),"x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"}
keys_to_keep = ['date_validthrough','title','url','external_apply_url','description_text', 'employment_type','salary_raw', 'seniority', 'linkedin_org_description', 'external_apply_url']
resume = "resume.docx"
api = os.getenv('OPENAI_API_KEY')
# Create an instance of the OpenAI client with API key in environment variables
client = OpenAI(
    api_key = api
)

# JobScraper as a class object
class JobScraper:
    def __init__(self, url, headers, jobs):
        self.url = url
        self.headers = headers
        self.jobs = jobs
    
    # query getJobOffers using members of JobScraper class
    def getJobOffers(self):
        try:
            job_offers = ["" for j in range(self.jobs)]
            # The actual search parameters
            querystring = {"limit":self.jobs,"offset":0,"order":"asc","title_filter":"\"Developer\"","description_filter":"Front End | Frontend","seniority":"Entry Level","location_filter":"\"United States\" OR \"United Kingdom\"","description_type":"text","type_filter":"FULL_TIME"}
            with requests.get(self.url, headers=self.headers, params=querystring) as response:
                if response.status_code == 200:
                    data = json.loads(response.text)
                    for l in range(self.jobs):
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
    
# Abstract Base Class
class IEmbeddingService(ABC):
    @abstractmethod
    def getEmbeddings(self, jobs:list, model:str):
        pass
# ChatGptEmbedding
class ChatGPTEmbeddingService(IEmbeddingService):
    def getEmbeddings(self, jobs, model):
        embeddings = []
        for string in jobs:
            string = string.replace("\n", " ")
            embedding = client.embeddings.create(input = [string], model=model).data[0].embedding
            embeddings.append(embedding)

        return embeddings
# the actual EmbeddingService that will be called
class EmbeddingService:
    def __init__(self, IEmbeddingService:IEmbeddingService):
        self.IEmbeddingService = IEmbeddingService
    
    def embeddings(self, jobs, model):
        return self.IEmbeddingService.getEmbeddings(jobs, model)



# Similarity Calculator with basic method rank that uses a seperate method to order indicies of nearest neighbors
class SimilarityCalculator:
    def __init__(self, embeddings, resume, model):
        self.embeddings = embeddings
        self.resume = resume
        self.model = model

    def distances_from_embeddings(self,
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

    def indices_of_nearest_neighbors_from_distances(self, distances) -> np.ndarray:
        return np.argsort(distances)

    def rank(self):
        query_embedding = self.embeddings[0]
        distances = self.distances_from_embeddings(query_embedding, self.embeddings, distance_metric="cosine")
        indices_of_nearest_neighbors = self.indices_of_nearest_neighbors_from_distances(distances)
        
        return indices_of_nearest_neighbors


# a simple resume converter using docx2txt
class resumeConverter:
    def __init__(self, resume):
        self.resume = resume
    
    def convertResume(self):
        doc = docx2txt.process(self.resume)
        doc = doc.replace("\n", " ")
        return doc



if __name__ == "__main__":
    ResumeReader = resumeConverter(resume)
    convertedResume = ResumeReader.convertResume() # read and convert resume

    Scraper = JobScraper(api_url, headers, 50) 
    jobs = Scraper.getJobOffers()
    jobs.insert(0, convertedResume) # get job offers, insert converted resume at start


    ChatGPT = ChatGPTEmbeddingService()
    embeddingService = EmbeddingService(ChatGPT)
    embedded = embeddingService.embeddings(jobs, "text-embedding-3-small") # create embedding service, get embeddings


    Calculator = SimilarityCalculator(embedded, resume, "text-embedding-3-small")
    top_jobs = Calculator.rank() # calculate top results


    topTen = ["" for i in range(10)] # create array

    for m, job in enumerate(top_jobs[1:11]):
        topTen[m] = jobs[job].replace("\n", " ")
    for topjob in topTen:
        print(topjob) # print top ten results.