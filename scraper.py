from requests_html import HTMLSession

class Scraper():
    
    def featuredNews(self):
        url = 'https://www.cbc.ca/news/canada'
        s = HTMLSession()
        r = s.get(url)
        # print(r.status_code)

        try:
            # ------------------------------
            #  Get all featured hightlights News
            # ------------------------------
            f_Highlight__div = r.html.find('div.featuredHighlights', first=True)
            f_Highlight__list = f_Highlight__div.find('a.card')
            
            featuredHighlights = getFeaturedHighlights(f_Highlight__list)

            
            # --------------------------------
            # Get all top stories
            # --------------------------------
            f_topStories__div = r.html.find('div.secondaryTopStories', first=True)
            f_topStories__list = f_topStories__div.find('a.card')

            topStories = getFeaturedTopStories(f_topStories__list)


            return {
                'message': 'success',
                'data': {
                    'topStories': topStories,
                    'featuredHighlights': featuredHighlights
                }
            }

        except:
            return {
                'message': "ERROR: Internal Server Error",
            }
    
    
    def allNews(self):
        url = 'https://www.cbc.ca/news/canada'
        s = HTMLSession()
        r = s.get(url)
        allNewsList = []

        # ------------------------------
        try:
            allNews__cards = r.html.find('a.card')
            for item in allNews__cards:
                global headline
                global thumbnail
                global newsLink
                global author__name
                global author__avatar
                global publishedOn
                global publishedDate
                global description

                newsLink = 'https://www.cbc.ca' + item.xpath('//a/@href')[0]

                # Parse thumbnail
                if(item.find('img', first=True) == None):
                    thumbnail = '#'
                else:
                    thumbnail = item.find('img', first=True).attrs['src']

                # Parse headline
                headline = item.find('h3.headline', first=True).text.strip()

                # Parse description
                if(item.find('div.description', first=True) == None):
                    description = ''
                else:
                    description = item.find('div.description', first=True).text.strip()
                
                # Parse author
                authorInfo = item.find('div.authorInfo', first=True)
                if(authorInfo != None):
                    author__name = item.find('div.authorName', first=True).text.strip()
                    author__avatar = item.find('figure.author-image > div.placeholder > img', first=True).attrs['src']
                else:
                    author__name = 'undefined'
                    author__avatar = '#'

                publishedOn = item.find('time.timeStamp', first=True).text.strip()
                publishedDate = item.find('time.timeStamp', first=True).attrs['datetime']
                

                allNewsList.append({
                    'headline' : headline,
                    'thumbnail' : thumbnail,
                    'newsLink' : newsLink,
                    # 'description': description,
                    'authorName' : author__name,
                    'authorImage' : author__avatar,
                    'publishedOn' : publishedOn,
                    'publishedDate' : publishedDate
                })


            return {
                'message': 'success',
                'data': allNewsList
            }
            # --------------------------
        except:
            return {
                'message': "ERROR: Internal Server Error"
            }

    
    def categories(self):
        return [
            {'id': 1, 'name': 'COVID-19', 'slug' : 'covid-19'},
            {'id': 2, 'name': 'Climate and Environment', 'slug' : 'climate'},
            {'id': 3, 'name': 'World', 'slug' : 'world'},
            {'id': 4, 'name': 'Politics', 'slug' : 'politics'},
            {'id': 5, 'name': 'Indigenous', 'slug' : 'indigenous'},
            {'id': 6, 'name': 'Opinion', 'slug' : 'opinion'},
            {'id': 7, 'name': 'Business', 'slug' : 'business'},
            {'id': 8, 'name': 'Health', 'slug' : 'health'},
            {'id': 9, 'name': 'Entertainment', 'slug' : 'entertainment'},
            {'id': 10, 'name': 'Science', 'slug' : 'science'},
            {'id': 11, 'name': 'Investigates', 'slug' : 'investigates'},
        ]


    def newsByCategory(self, category):    
        url = f'https://www.cbc.ca/news/{category}'
        s = HTMLSession()
        r = s.get(url)
        allNewsList = []

        # ------------------------------
        try:
            allNews__cards = r.html.find('a.card')
            for item in allNews__cards:
                global headline
                global thumbnail
                global newsLink
                global author__name
                global author__avatar
                global publishedOn
                global publishedDate
                global description

                newsLink = 'https://www.cbc.ca' + item.xpath('//a/@href')[0]

                # Parse thumbnail
                if(item.find('img', first=True) == None):
                    thumbnail = '#'
                else:
                    thumbnail = item.find('img', first=True).attrs['src']

                # Parse headline
                if(item.find('h3.headline', first=True) != None):
                    headline = item.find('h3.headline', first=True).text.strip()
                else:
                    headline = ''

                # Parse description
                if(item.find('div.description', first=True) == None):
                    description = ''
                else:
                    description = item.find('div.description', first=True).text.strip()
                
                # Parse author
                authorInfo = item.find('div.authorInfo', first=True)
                if(authorInfo != None):
                    author__name = item.find('div.authorName', first=True).text.strip()
                    author__avatar = item.find('figure.author-image > div.placeholder > img', first=True).attrs['src']
                else:
                    author__name = 'undefined'
                    author__avatar = '#'

                if(item.find('time.timeStamp', first=True) != None):
                    publishedOn = item.find('time.timeStamp', first=True).text.strip()
                    publishedDate = item.find('time.timeStamp', first=True).attrs['datetime']
                else:
                    publishedOn = ''
                    publishedDate = ''


                allNewsList.append({
                    'headline' : headline,
                    'thumbnail' : thumbnail,
                    'newsLink' : newsLink,
                    'description': description,
                    'authorName' : author__name,
                    'authorImage' : author__avatar,
                    'publishedOn' : publishedOn,
                    'publishedDate' : publishedDate
                })


            # --------------------------
            return {
                "message": 'success',
                "data": allNewsList
            }
        
        except:
            return {
                'message': "ERROR: Internal Server Error"
            }




# ----------------------------
def getFeaturedHighlights(hightlightsList):
    featuredHighlights = []

    for item in hightlightsList:
            global headline
            global author__name
            global author__avatar
            global description
            global img__full
            global img__sizes
            global img__srcset
        
            link = 'https://www.cbc.ca' + item.xpath('//a/@href')[0]
            
            # image attributes
            if(item.find('div.placeholder > img', first=True) != None):
                img__full = item.find('div.placeholder > img', first=True).attrs['src']
                img__srcset = item.find('div.placeholder > img', first=True).attrs['srcset']
                img__sizes = item.find('div.placeholder > img', first=True).attrs['sizes']
            else:
                img__full = ''
                img__sizes = ''
                img__srcset = ''

            if(item.find('h3.headline', first=True) != None):
                headline = item.find('h3.headline', first=True).text.strip()

            if(item.find('div.description', first=True) != None):
                description = item.find('div.description', first=True).text.strip()

            authorInfo = item.find('div.authorInfo', first=True)
            if(authorInfo != None):
                author__name = item.find('div.authorName', first=True).text.strip()
                author__avatar = item.find('figure.author-image > div.placeholder > img', first=True).attrs['src']
            else:
                author__name = 'undefined'
                author__avatar = '#'


            publishedOn = item.find('time.timeStamp', first=True).text.strip()
            publishedDate = item.find('time.timeStamp', first=True).attrs['datetime']
            
            
            featuredHighlights.append({
                'headline' : headline,
                'thumbnail' : { 'src' : img__full, 'srcset': img__srcset, 'sizes' : img__sizes },
                'description' : description,
                'newsLink': link,
                'authorName': author__name,
                'authorImage': author__avatar,
                'publishedOn': publishedOn,
                'publishedDate': publishedDate
            })

    return featuredHighlights


def getFeaturedTopStories(topstoryList):
    featuredTopStories = []

    for item in topstoryList:
            global headline
            global author__name
            global author__avatar
            global publishedOn
            global publishedDate

            link = 'https://www.cbc.ca' + item.xpath('//a/@href')[0]

            if(item.find('h3.headline', first=True) != None):
                headline = item.find('h3.headline', first=True).text.strip()

            authorInfo = item.find('div.authorInfo', first=True)
            if(authorInfo != None):
                author__name = item.find('div.authorName', first=True).text.strip()
                author__avatar = item.find('figure.author-image > div.placeholder > img', first=True).attrs['src']
            else:
                author__name = 'undefined'
                author__avatar = '#'

            if(item.find('time.timeStamp', first=True) != None):
                publishedOn = item.find('time.timeStamp', first=True).text.strip()
                publishedDate = item.find('time.timeStamp', first=True).attrs['datetime']
            

            featuredTopStories.append({
                'headline' : headline,
                'newsLink': link,
                'authorName': author__name,
                'authorImage': author__avatar,
                'publishedOn': publishedOn,
                'publishedDate': publishedDate
            })

    return featuredTopStories
# ----------------------------

