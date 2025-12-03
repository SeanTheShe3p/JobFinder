# Refactored Code

## Single Purpose and Dependency Inversion

    1. Single Responsibility was an obvious choice because it really is the most basic, and necessary principle. Code that is simply a script is hard to follow and a lot of ease of readability comes from having single purpose classes, everything is nicely labeled in dot notation and instances of objects are created allowing an amount of reusability in the code. 
```Scraper = JobScraper(api_url, headers, 50)
jobs = Scraper.getJobOffers()```
    vs
`job_list = pull_api_data(api_url, headers, 99)`
    Ironically for this use it actually made the main function longer, but the traceability of the function calls is night and day obvious, especially in
`top_jobs = compare_data(job_list, resume)`
    which initally had a jumble of different functions called and was essentially one monolith, is now
`ChatGPT = ChatGPTEmbeddingService()
embeddingService = EmbeddingService(ChatGPT)
embedded = embeddingService.embeddings(jobs, "text-embedding-3-small")
Calculator = SimilarityCalculator(embedded, resume, "text-embedding-3-small")
top_jobs = Calculator.rank()```


    2. Dependency Invesion was the next implementation due to the complexity of embedding services, and for security purposes, it makes sense to abstract away from the embedding service by implementing an interface that any embedding services could use. I did this by using the abstract base class and giving ChatGPT its own implementation so that if someone were to want to use a Gemini or DeepSeek embedding model that could be done much easier. 
```
class IEmbeddingService(ABC):
    @abstractmethod
    def getEmbeddings(self, jobs:list, model:str):
        pass

class ChatGPTEmbeddingService(IEmbeddingService):
    def getEmbeddings(self, jobs, model):
        (...)
        return embeddings

class EmbeddingService:
    def __init__(self, IEmbeddingService:IEmbeddingService):
        self.IEmbeddingService = IEmbeddingService
    
    def embeddings(self, jobs, model):
        return self.IEmbeddingService.getEmbeddings(jobs, model)```

