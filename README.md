# LinkedIn Job Finder
This app uses an API to compare job postings of a particular type to any docx resume. For instance, one could search for landscaping jobs with a landscaping resume. The app uses a second API, OpenAi, to create embeddings of the jobs and your resume and compare them, using cosine similarity. The app then outputs "LinkedIn.txt" with your top 10 job postings.

## installation:
Requirements: Conda

1. Create Conda environment by running
    `conda env create -f environment.yml`
2. Activate environment by running
    `conda activate JobFinder`
3. Place resume in folder directory titled "resume.docx"
4. run
    `python linkedInJobFinder.py`

## Docker Container
There is a docker image of the program also available for ease of use,
1. run
`docker pull gamebulese/jobfinder:latest`
2. run
`docker run --rm gamebulese/jobfinder:latest`
3. Success!


## tests:
1. run
    `python -m pytest`
    test 1 - create a fake api call monkeypatching requests
    test 2 - use a mock embedding service to test abstract base class by creating a mock interface
    test 3 - create fake embeddings and test SimilarityCalculator for rank()
    test 4 - convert a fake resume, monkeypatch method to return mock value

## Usage:
    2025-11-08T00:34:56Senior Front-End Developer - React Native & Web (DevOps-First) https://www.linkedin.com/jobs/view/senior-front-end-developer-react-native-web-devops-first-at-sports-profile-network-4312390561 None75% Front-End (React Native + React Web) + 25% Backend (TypeScript Node.js). You'll modernize our mobile app, build responsive web experiences, and develop the backend-for-frontend service that power them—all with a strong emphasis on deployment automation and pipeline reliability.  The Technical Stack:  Mobile (Primary - ~50%): - React Native / Expo - TypeScript strict mode - EAS builds & deployments - iOS & Android platforms  Web (Secondary - ~25%): - React + TypeScript - Vite build tooling - Responsive design (mobile-first) - Component library development  Backend-for-frontend (25%): - Node.js + TypeScript - RESTful APIs - Microservices integration   What You'll Do:  Mobile Development (50%) - Lead migration from bare React Native to Expo managed workflow - Build and refactor React Native components with TypeScript - Implement new features while modernizing legacy code - Optimize app performance and bundle size - Own iOS & Android deployments via EAS  Web Development (25%) - Build responsive, accessible React web applications - Implement reusable components from Figma designs - Use modern tooling: React + TypeScript + Vite - Create reusable component libraries - Ensure cross-browser compatibility and performance  Backend Development (25%) - Design and build TypeScript Node.js APIs (REST or GraphQL) - Extract business logic from front-end to backend services - Design database schemas and optimize queries - Implement authentication and authorization - Write API documentation and tests  DevOps (Ongoing) - Maintain and improve GitHub Actions CI/CD pipelines - Manage EAS build configurations for mobile - Deploy backend services to cloud platforms - Optimize build times and pipeline reliability - Document deployment processes   Our Mission: At SPIN, we believe that sports should bring families and communities together, not create chaos through fragmented technology. We're building the ultimate integration platform that consolidates the scattered world of youth sports apps into one seamless experience.['FULL_TIME']NoneMid-Senior levelThe first all sports social networkNone.....
    
## Contrubuting to the project:
    If you wish to contribute, you will need your own API keys.

## License:
    None

## Contact:
     email me: seantheshe3p@gmail.com

* * *

#### APIs I tried:
    https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/linkedin-job-search-api
    https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/active-jobs-db

#### Documentation of APIs:
    Unfortunately upon initally searching I found that the API I most wanted required a "partnership" with indeed, and thus decided that using the top API on rapidapi.com was then the next best, albiet expensive, I tried two different APIs and found the more significant results were from one, as the second one I tested, although advertising many more jobs, returned only a couple even with basically plain parameters. I played with various parameters especially the offset, title filter, seniority filter, and various ai filters, and found that most created too restrictive of an environment, for instance, "Entry Level Android Developer" returns zero results. whereas "Web Developer" returns over 100. Ultimately I used the description filter as the best means of getting relevant job postings. Some formatting was necessary, I needed to add spaces around the urls(I thought none of the jobs were real for quite some time), and I removed the newlines.

#### Resume Preprocessing:
    I decided I wanted to gain some insight into the types of jobs available, so I went with a resume that is based around types of projects I am working on today. I dont have any relevant work experience, so that is the best I can do. I took the time to try and get my .docx resume to work and I eventually managed to pull decently formatted data using docx2txt. I had a few issues with the formatting of the origional resume template, and went with a more basic one, it probably wouldnt have mattered much to the embedding, if the headers for each section are in a different location, but I switched it anyways. 

#### Embeddings:
    This was the most difficult step before I searched the utility file that OpenAi has their functions listed on I was scouring the internet trying to get the API to connect, which is rather rediculous, because I have used APIs in the past. Getting the embeddings returned a lot more data than I was expecting it to use, I suppose it must have done an embedding for each token. Very neat software. 
 
#### Cosine Similarity:
    Cosine Similarity is something I have heard of but havent had the opportunity to try, I was very excited to see the results. Overall I think it returned accurate results. It definately found my ASP.Net Core experience, web developer skills, sometimes it doesn't nail I dont have work experience, but that could also be the lacking of roles in the API that are "Junior" or "Entry Level" as they both return very few results when tested. Ultimately I think a clean text file with one job per line was the best formatting, links after the titles, as it is easy to read and easy to navigate.