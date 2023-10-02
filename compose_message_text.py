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
deal_one = '''<a target="_blank" href="https://hotellook.tp.st/TJUioPBZ">It's travel season, get a great deal on hotel accommodations.</a> <br> '''

deal_two = '''<a target="_blank" href="https://hotellook.tp.st/TJUioPBZ">Need to get away? Get a great deal on your next hotel stay.</a> <br> '''

def compose_message_html():
  final_string = ""
  final_string += "<h3>Always see the positive side... even if it's ridiculous.</h3>"
  final_string += """<h6>These articles were intended to be written as overly optimistic satire while preserving the facts, however they may not always be completely factual. Please visit the "Inspiration for this satire" links for more factual details. </h6>"""
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
    final_string += """<br> <table style="width: 100%;">
    <tr>
        <td align="center">
            <a href="https://twitter.com/intent/tweet?text=Check out this new ridiculously positive newsletter.&url=https://toogood.news&hashtags=toogoodnews,positive,goodnews" target="_blank">
                <img height="20" src="https://about.twitter.com/content/dam/about-twitter/x/brand-toolkit/logo-black.png.twimg.1920.png" style="border-radius:3px;display:block;" width="20">
            </a>
        </td>
    </tr>
</table> <br>"""
    final_string += deal_two      
    final_string += """<div style="text-align: center;font-size:12px;"><p>This email is from TooGood.news - ADM OFFERINGS LLC, USA for more info visit <a href>https://toogood.news</a></p></div><br><div style="text-align: center;font-size:12px;"><a href="[[UNSUB_LINK_EN]]">click here to unsubscribe</a></div>"""
  print("returning final_string")

  # save a txt copy of the final string
  with open("final_string_text.txt", "w") as txt_file:
    txt_file.write(final_string)
  
  return final_string
  
  
if __name__ == "__main__":
  bring_order_gptd_articles()
  compose_message_html()
