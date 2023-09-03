import csv


'''
bring_order_gptd_articles() function reorgs the csv so that the compose_message_html() can do the final processing and create the html to be sent and output a multiline string containing the full html for use with the Mailjet schedule & send module. Also takes into consideration adding of advertising html.
'''

def bring_order_gptd_articles():
  '''This function runs the process of taking gptd_articles.csv and reordering it so it can be properly processed in the ###### function'''

  # reorder the csv for into proper order for next process
  # Open the input and output CSV files 
  with open('gptd_articles.csv', 'r') as input_file, open('ordered_gptd_articles.csv', 'w', newline='') as output_file: 
    # Create a DictReader object for the input file 
    reader = csv.DictReader(input_file) 
    # Define the desired column order 
    column_order = ['Title', 'Contents', 'Link'] 
    # Create a DictWriter object for the output file with the desired column order 
    writer = csv.DictWriter(output_file, fieldnames=column_order) 
    # Write the header row to the output file 
    writer.writeheader() 
    # Iterate over the rows in the input file 
    for row in reader: 
      # Create a new dictionary with the reordered columns 
      reordered_row = {column: row[column] for column in column_order} 
      # Write the reordered row to the output file 
      writer.writerow(reordered_row)
   
#####

#Advertising offer html deals:
deal_one = '''<a target="_blank" href="https://www.amazon.com/dp/B00NB86OYE/?ref_=assoc_tag_ph_1485906643682&_encoding=UTF8&camp=1789&creative=9325&linkCode=pf4&tag=suavevibecom-20&linkId=5bff7607fba3c6d8d0e50ebed256f681">Try Audible Premium Plus and Get Up to Two Free Audiobooks</a> <br> '''

deal_two = '''<a target="_blank" href="https://www.amazon.com/hz/audible/gift-membership-detail?tag=suavevibecom-20&ref_=assoc_tag_ph_1524210806852&_encoding=UTF8&camp=1789&creative=9325&linkCode=pf4&linkId=802c2f58fb3ba22a0ee796f22fbec256">Give the Gift of an Audible Membership</a> <br> '''

def compose_message_html():
  final_string = ""
  final_string += "<h3>Always see the positive side...</h3>"
  final_string += '''<img src="https://toogood.news/wp-content/uploads/2023/08/toogoodtxt175.png" alt="Image description" style="display: block; margin: 0 auto;"><br> '''
  final_string += deal_one
  # Title, Contents, Link ----temp
  with open("ordered_gptd_articles.csv", "r") as file:
    #create reader object
    reader = csv.DictReader(file)
    #iterate over each row in csv
    for row in reader:
      #access each item in row independently
      for column_title, item in row.items():
        #perform various operations based on column title
        if column_title == 'Title':
          final_string += f"<h3>{item}</h3>"
        elif column_title == 'Contents':
          final_string += " <br> "
          item_with_line_breaks = item.replace("\n","<br>")
          final_string += f"<p>{item_with_line_breaks}</p>"
        elif column_title == 'Link':
          final_string += "<br>"
          final_string += f'<a href="{item}"target="_blank">Inspiration for this satire</a><br>'
          final_string += " <br> "
    final_string += deal_two      
    final_string += """<div style="text-align: center;font-size:12px;"><p>As an Amazon Associate we earn from qualifying purchases. This email is from TooGood.news - ADM OFFERINGS LLC, USA for more info visit <a href>https://toogood.news</a></p></div><br><div style="text-align: center;font-size:12px;"><a href="[[UNSUB_LINK_EN]]">click here to unsubscribe</a></div>"""
  print("returning final_string")
  return final_string
  
  
if __name__ == "__main__":
  bring_order_gptd_articles()
  compose_message_html()
