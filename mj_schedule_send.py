# import the mailjet wrapper
from mailjet_rest import Client
import os
from datetime import datetime, timedelta

'''
This code is to schedule and send a Mailjet campaign when given the html email as a string and the text only email string as parameters.
'''

# Get your environment Mailjet keys
MJ_API_KEY = os.environ['MJ_APIKEY_PUBLIC']
MJ_API_SECRET = os.environ['MJ_APIKEY_PRIVATE']

def schedule_send_campaign(email_html, email_txt):

  '''
  Schedule and send a Mailjet campaign when given the html email as a string and the text only email string as parameters. First parameter of the schedule_send_campaign function takes the multiline string of the email in html format. Second parameter of the schedule_send_campaign function takes the multiline string of the text only version of the email to schedule and send.
  '''
  mailjet = Client(auth=(MJ_API_KEY, MJ_API_SECRET), version='v3')
  
  
  
  # Create campaign draft first
  data = {
    'Locale': 'en_US',
    'Sender': 'TooGoodNews',
    'SenderEmail': 'noreply@mailing.toogood.news',
    'Subject': 'Too Good News',
    'ContactsListID': '80961', #81981 = debug, 80961 = live
    'Title': 'Too Good Newsletter'
  }
  result = mailjet.campaigndraft.create(data = data)
  #print(result.status_code)
  #print(result.json())
  
  json_dict = dict(result.json())
  
  print(json_dict['Data'][0]['ID']) #this selects the draft id
  print(json_dict['Data'][0]['CreatedAt']) #created at time
  
  draft_id = json_dict['Data'][0]['ID'] #id of draft, int
  draft_creation_time = json_dict['Data'][0]['CreatedAt'] #str
  
  
  ############
  
  
  # Next we add the content to the draft
  detail_data = {
    'Headers': "object",
    'Html-part': email_html,
    'MJMLContent': "",
    'Text-part': email_txt 
  }
  
  result = mailjet.campaigndraft_detailcontent.create(id = draft_id, data = detail_data)
  
  print(result.status_code)
  print(result.json())
  
  #############
  
  
  # Here we can send a Test email of the draft
  test_data = {
    'Recipients': [
      {
        "Email": "info@toogood.news",
        "Name": "TooGoodNews Crew"
      }
    ]
  }
  result = mailjet.campaigndraft_test.create(id = draft_id, data = test_data)
  print(result.status_code)
  print(result.json())
  
  
  #############

  # create a datetime string in valid format for +3 hrs send
  
  current_time = datetime.utcnow()
  sched_time = current_time + timedelta(hours=3)
  dt_string = sched_time.strftime('%Y-%m-%dT%H:%M:%SZ')
  print('Scheduled time is: '+dt_string)
  
  #############
  
  # Schedule the campaign to send after a delay (3hrs)
  sched_data = {
    'Date': dt_string
  }
  result = mailjet.campaigndraft_schedule.create(id = draft_id, data = sched_data)
  print('Scheduled campaign info: ')
  print(result.status_code)
  print(result.json())

# Reverts to sample code if run as main:
if __name__ == "__main__":
  # these have html placeholder txt, function parameters would typically override
  email_html = """<h3>Dear readers, welcome to Too Good News!</h3><br />May the news be ridiculously good! <br> <div style="text-align: center;font-size:12px;">
	<p>This email is from TooGood.news - ADM OFFERINGS LLC, USA for more info visit <a href>https://toogood.news</a></p>
</div>
<br>
<div style="text-align: center;font-size:12px;">
	<a href="[[UNSUB_LINK_EN]]">click here to unsubscribe</a>
</div>"""
  email_txt = "" #empty string, only sending html version
  schedule_send_campaign(email_html, email_txt)