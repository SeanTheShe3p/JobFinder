import refactoredLinkedInJobFinder as mod
from refactoredLinkedInJobFinder import JobScraper, EmbeddingService, IEmbeddingService, SimilarityCalculator, resumeConverter

import json
import numpy as np
import pytest
import requests
import docx2txt

# set the fake job scraper return value
def test_job_scraper(monkeypatch):
    fake_json = json.dumps([
        {"title": "Developer", "url": "http://api.com"}
    ])

# create the instance of the fake job scraper with methods to enable monkeypatching
    class PatchResponse:
        def __init__(self):
            self.status_code = 200
            self.text = fake_json
        def __enter__(self):
            return self
        def __exit__(self, *a):
            pass
        
# function to return fake response
    def fake_get(*a, **kw):
        return PatchResponse()

# set keys to keep and get request
    monkeypatch.setattr(mod, "keys_to_keep", ["title", "url"])
    monkeypatch.setattr(mod.requests, "get", fake_get)

# create mock JobScraper and run getJobOffers()
    scraper = JobScraper("https://wwww.fakeapidomain.com", {}, 1)
    result = scraper.getJobOffers()

    assert result == ["Developer http://api.com "]




class MockEmbeddingService(IEmbeddingService):
    def getEmbeddings(self, jobs, model):
        return [[1, 0]]  # create fake embeddings

# test false embedding service to return fake embeddings
def test_embedding_service_with_mock():
    mockEmbeddingService = MockEmbeddingService()
    embeddingService = EmbeddingService(mockEmbeddingService)

    result = embeddingService.embeddings(["hello"], "model")

    assert result == [[1, 0]]  # received from mock service




# create list of fake embeddings, one the same as first one not.
def test_similarity_calculator_rank():
    embeddings = [[1, 0],[1, 0],[0, 1]]

# run similarityCalc and rank() normally
    calc = SimilarityCalculator(embeddings, "resume", "model")
    result = calc.rank()

# expected order is query, similar, different
    assert np.array_equal(result, np.array([0, 1, 2]))





# create fake resume to return
def test_resume_converter(monkeypatch):
    def fake_resume(path):
        return "Hello World"

# set fake resume
    monkeypatch.setattr(docx2txt, "process", fake_resume)

    resume = resumeConverter("fake.docx")
    result = resume.convertResume()
# return fake value
    assert result == "Hello World"

