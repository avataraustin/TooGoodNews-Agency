import csv
import os
from newsdataapi import NewsDataApiClient


'''
This module uses newdata api to gather top news stories and save in csv
'''


def gather_top_news():
  api = NewsDataApiClient(apikey=os.environ['NEWS_API'])
  
  # You can pass empty or with request parameters {ex. (country = "us")}
  response = api.news_api(q = "AP", country = "us", category = "top", language = "en")
  
  links = []
  titles = []
  descriptions = []
  contents = []
  
  #filters to use to discard stories
  links_filter = ["newyorker.com/humor"]
  contents_filter = ["rewritten"]
  
  #iterate over response sorting for later adding to a csv file
  for story in response['results']:
    #check filter lists for not in story["description"] or
    # story["link"]  #avoid getting sued filter
    if not (any(string in story["description"] for string in contents_filter)) and not (any(string in story["link"] for string in links_filter)):
      links.append(story["link"])
      titles.append(story["title"])
      descriptions.append(story["description"])
      contents.append(story["content"])
    
  
  zipped_news = zip(links, titles, descriptions, contents, strict=True)
  
  #store the response results in a csv file for later use
  with open('stored_articles.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Link', 'Title', 'Description', 'Contents']) # write header row
    writer.writerows(zipped_news) # write data rows
  
if __name__ == "__main__":
  gather_top_news()