import csv
import os
from newsdataapi import NewsDataApiClient
from gather_news_data import gather_top_news
import openai
import time
import gpt_rephrase_news
import compose_message_text
from mailjet_rest import Client
from datetime import datetime, timedelta
import datetime
import mj_schedule_send
import logging


#logging config
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt= "%d-%b-%y %H:%M:%S", level=logging.INFO)

logger = logging.getLogger(__name__)

# Days to deliver the news
newsdays = ['Tuesday', 'Thursday', 'Saturday']

while True:
  print ("Restarting...")

  xday = datetime.datetime.now() #store todays date info
  print("current day: ", xday.strftime("%A"))
  xdaymdy = xday.strftime("%x") #date in mo/da/yr format
  
  if xday.strftime("%A") in newsdays: #only run on newsdays  
    print("current utc hour:", datetime.datetime.utcnow().strftime("%H"))
    #below code causes to execute between 6am-8am (12-14 utc) cent time
    if int(datetime.datetime.utcnow().strftime("%H")) >= 12 and int(datetime.datetime.utcnow().strftime("%H")) < 14:
      # check status file to see if app has already run today
      with open("status.txt", "r") as f:
        fetched = f.readline()
      if fetched != xdaymdy: #if final check is a go, we run the app  
          
        # run the module for gathering news stories, outputs
        # stored_articles.csv file for use later
        try:
          gather_top_news()
          logger.info("gather_top_news() ran without error")
        except:
          logger.error("gather_top_news error triggered")

        
        # run the module for gpt processing of articles & titles
        # outputs gptd_articles.csv for later use
        try:
          gpt_rephrase_news.produce_content_csv()
          logger.info("gpt_rephrase_news.produce_content_csv ran without error")
        except:
          logger.error("gpt_rephrase_news.produce_content_csv error triggered")

        
        # run 1st func from module to reorder csv to proper format
        # produces ordered_gptd_articles.csv 
        try:
          compose_message_text.bring_order_gptd_articles()
          logger.info("compose_message_text.bring_order_gptd_articles ran w/o error")
        except:
          logger.error("compose_message_text.bring_order_gptd_articles error triggered")

        
        # run 2nd fun from module to produce final html format
        # func returns final_string of html & stores in var
        try:
          html_string = compose_message_text.compose_message_html()
          logger.info("compose_message_text.compose_message_html ran w/o error")
        except:
          logger.error("compose_message_text.compose_message_html error triggered")

        
        # run mj_schedule_send module func to send the final html
        # to mailjet send test email & schedule campaign for 3hrs later
        # first param is html email, 2nd param is txt-only email which
        # is not configured so we just pass an empty string
        try:
          mj_schedule_send.schedule_send_campaign(html_string, "")
          logger.info("mj_schedule_send.schedule_send_campaign(html_string, "") ran w/o error")
        except:
          logger.error("mj_schedule_send.schedule_send_campaign(html_string, "") error triggered")

        
        # open a file called status.txt and (over)write to it to store
        # todays m/d/yr date to the file so we can avoid duplicate sends
        with open("status.txt", "w") as f:
          f.write(xday.strftime("%x"))
      else:
        time.sleep(3600) # sleep 1hr if status file already has todays date
    else:
      time.sleep(2700) # sleep 45 min. if is a newsday but not 12-14 UTC (6-8am centrl)
  else:
    time.sleep(3600) # sleep 1hr if its not a newsday
    