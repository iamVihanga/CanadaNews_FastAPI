from fastapi import FastAPI
from scraper import Scraper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
scraperInstance = Scraper()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def getAllNews():
    return scraperInstance.allNews()

@app.get('/featured')
async def getFeaturedNews():
    return scraperInstance.featuredNews()

@app.get('/categories')
async def getAllCategories():
    return scraperInstance.categories()

@app.get('/news/{category}')
async def getNewsByCategory(category):
    return scraperInstance.newsByCategory(category)
