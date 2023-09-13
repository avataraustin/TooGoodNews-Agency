import openai
import csv
import os
import time


'''
This module is a set of functions to work with a csv file generated from a different module. The csv file to work with contains news story link, title, description, and content. The main produce_content_csv() function called 2 other functions designed to use openai gpt model to create a new title and new article and then save results to a file called "gptd_articles.csv" that contains "Link", "Title", and "Content" collumns in the new csv. 
'''

openai.api_key = os.environ['OPENAI_API_KEY']

#create function for gpt processing to create a title
def gpt_to_title(txt_chunk):
  '''
  function takes a string or string concatenated variable as txt_chunk and processes it with openai gpt model to rephrase text into a new article title, returned as a string.
  '''
  response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
    {"role": "system",
    "content": "You are a ridiculously upbeat news article writer"},
    {"role": "user",
    "content": "Rephrase this into a ridiculously positive short descriptive article title in English: " + txt_chunk}
    ]
  )

  return response["choices"][0]["message"]["content"]

def gpt_article_rephrase(txt_content):
  '''
  function takes a string as txt_content and processes it with openai gpt model to rephrase text into a ridiculously positive new article, returned as a string.
  '''
  response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-16k",
    messages = [
    {"role": "system",
    "content": "You are a ridiculously upbeat news article writer"},
    {"role": "user",
    "content": "Rephrase this into a ridiculously positive and enthusiastically optimistic article. Put a ridiculous and positive spin on the article. Summarize to reduce overall length. Be certain to exaggerate any potentially positive aspects: " + txt_content}
    ]
  )

  return response["choices"][0]["message"]["content"]  


def produce_content_csv():
  '''
  Processes a csv called 'stored_articles.csv', combines title and description before sending to the gpt_to_title function. Runs both gpt functions and stores all the gpt processed stories in a new csv file called 'gptd_articles.csv'. Seems to take about 7 min. to run a 10 story csv, including the time.sleep()'s added to avoid api errors.
  '''
  links = []
  titles = []
  descriptions = []
  contents = []
  
  with open("stored_articles.csv", "r") as file:
    #create csv reader object
    reader = csv.DictReader(file)
    #iterate over each row in csv
    for row in reader:
      #access each item in row independently
      for column_title, item in row.items():
        # perform various operations based on column title
        if column_title == 'Link':
          links.append(item)
        elif column_title == 'Title':
          titles.append(item)
        elif column_title == 'Description':
          descriptions.append(item)
        elif column_title == 'Contents':
          contents.append(item)
          
  #combine title & description before gpt
  combo_titles = [x + " " + y for x, y in zip(titles, descriptions)]
  
  #place to store gpt'd titles and contents
  gpt_titles = []
  gpt_contents = []
  
  for story in combo_titles:
    gpt_titles.append(gpt_to_title(story))
    time.sleep(20)
    print('processing gpt title')
    
  for story in contents:
    gpt_contents.append(gpt_article_rephrase(story))
    time.sleep(60)
    print('processing gpt content')
    
  zipped_gpt_news = zip(links, gpt_titles, gpt_contents)

  with open("gptd_articles.csv", "w", newline = "") as f:
    writer = csv.writer(f)
    writer.writerow(['Link', 'Title', 'Contents'])
    writer.writerows(zipped_gpt_news)

if __name__ == "__main__":
  produce_content_csv()