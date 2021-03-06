
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth
import ssl
import urllib
import re
from fast_app.models import tenure_raw

#### Here is where you create your API to pull data.
#### You need a scheduler to repeat this task
#### And also configure apps.py to run the scheduler
#### Credits to https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6

def _pull_and_update():
    print("Executing pull_and_update now: ",datetime.now())


    #### To overcome SSL error
    ssl._create_default_https_context = ssl._create_unverified_context




    #### request.get doesnt work
    #### New link is inserted into the page everyday. To get the latest link,
    #### I first find all the links in the previous page
    ####
    try:
        with urllib.request.urlopen("https://fast.bnm.gov.my/fastweb/public/FastPublicBrowseServlet.do?mode=MAIN&taskId=PB030100") as response:
            html = response.read()
            response.close()

        main_soup = BeautifulSoup(html, 'lxml')


        links_dict = {
            'mgs':[],
            'mgi':[],
        }

        #### Getting all interested hrefs
        #### Credits: https://pythonspot.com/extract-links-from-webpage-beautifulsoup/
        for link in main_soup.findAll('a',attrs={'href':re.compile("^Public")}):
            if '200700000001' in link.get('href'):
                links_dict['mgs'].append(link.get('href'))
            elif '200700000002' in link.get('href'):
                links_dict['mgi'].append(link.get('href'))
                # print(link.get('href'))

        #### The latest updated page always appears to be the first link (Hopefully)
        latest_page = [links_dict['mgs'][0], links_dict['mgi'][0]]

        # for link in links[:10]:
        #### Read the latest html after getting the link
        for latest_page in latest_page:
            try:
                with urllib.request.urlopen("https://fast.bnm.gov.my/fastweb/public/"+ latest_page) as response:
                    html = response.read()
                    response.close()
                    # print (html)

                soup = BeautifulSoup(html, 'lxml')
                tables = soup.find("table")

                #### Best filter so far to get the table I want
                tables_data = tables.findAll(lambda tag: tag.name =='tr' and tag.has_attr('class'))

                tenure_rate = []
                for tr in tables_data:
                    td = tr.find_all('td')
                    row = [tr.text for tr in td]
                    tenure_rate.append(row)
                # print(tenure_rate)


                #### Below is the output of tenure_rate
                #  ['24/01/20203-yr Reopening of MGS 03/23 3.480%'],
                #  ['\n\n'],
                #  ['Government Securities (Conventional) New as at 21/01/2020 '],
                #  ['BNMN BAND 1', '2.980'],
                #  ['BNMN BAND 4', '2.972'],
                #  ['BNMN BAND 7', '2.975'],
                #  ['BNMN BAND 10', '2.979'],
                #  ['MTB BAND 1', '2.980'],
                #  ['MTB BAND 4', '2.972'],
                #  ['MTB BAND 7', '2.975'],
                #  ['MTB BAND 10', '2.979'],
                #  ['MGS 1 YEAR', '2.960'],
                #  ['MGS 2 YEARS', '3.020'],
                #  ['MGS 3 YEARS', '3.042'],
                #  ['MGS 4 YEARS', '3.124'],
                #  ['MGS 5 YEARS', '3.157'],
                #  ['MGS 6 YEARS', '3.216'],
                #  ['MGS 7 YEARS', '3.265'],
                #  ['MGS 8 YEARS', '3.276'],
                #  ['MGS 9 YEARS', '3.293'],
                #  ['MGS 10 YEARS', '3.291'],
                #  ['MGS 15 YEARS', '3.490'],
                #  ['MGS 20 YEARS', '3.593'],
                #  ['MGS 30 YEARS', '4.010']]

                #### Extrating the date of the page
                match = re.search(r'\d{2}/\d{2}/\d{4}', tenure_rate[2][0])
                consolidated_date = datetime.strptime(match.group(), '%d/%m/%Y').date()

                #### Differentiate model with different group type
                #### Eg. Government Securities (Conventional), Government Securites (Islamic)
                group = ' '.join(tenure_rate[2][0].split()[:3])

                #### Saving model objects
                def save_data_to_model(tenure_rate):
                    #### Remove unrelevant items in list
                    tenure_rate = [items for items in tenure_rate if len(items)>1]
                    print(tenure_rate)

                    for each_tenure in tenure_rate:
                        new_item = tenure_raw.objects.create(tenure=each_tenure[0],rate=each_tenure[1],created_date=consolidated_date,group=group)



                #### Ingest data into model only if its new data
                if tenure_raw.objects.filter(group = group).last() is not None:
                    if consolidated_date == tenure_raw.objects.filter(group = group).last().created_date:
                        print (group,"No new data. Not saving data into model")
                    else:
                        save_data_to_model(tenure_rate)
                else:
                    save_data_to_model(tenure_rate)

                print("pull_and_update Done: ",datetime.now())
                # return None

            except urllib.error.URLError as e:
                print (e)
                print ("Maybe check your internet connection?")


    except urllib.error.URLError as e:
        print (e)
        print ("Maybe check your internet connection?")
