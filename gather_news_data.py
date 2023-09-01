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
  
  #iterate over response sorting for later adding to a csv file
  for story in response['results']:
    if "rewritten" not in story["description"]: #avoid getting sued filter
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