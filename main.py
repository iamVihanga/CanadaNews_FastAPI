from fastapi import FastAPI
from scraper import Scraper

app = FastAPI()
scraperInstance = Scraper()

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
