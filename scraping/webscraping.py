from bs4 import BeautifulSoup as bs
import datetime,requests,urllib.parse

def datef(date):
    return date[:2]+'-'+date[2:4]+'-'+date[-2:]

def scraping(link,d1,d2):
    date1 = datetime.datetime.strftime(datetime.datetime.strptime(d1, "%Y-%m-%d"), '%d-%m-%y')
    date2 = datetime.datetime.strftime(datetime.datetime.strptime(d2, "%Y-%m-%d"), '%d-%m-%y')
    date_list = []
    start = datetime.datetime.strptime(date1, '%d-%m-%y')
    end = datetime.datetime.strptime(date2, '%d-%m-%y')
    step = datetime.timedelta(days=1)
    while start<=end:
        date_list.append(start.strftime("%d-%m-%y"))
        start+=step
    url = link
    # url = 'http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm'
    response = requests.get(url)
    notice_date = {}
    soup = bs(response.text,'html.parser')

    for a in soup.find_all('a',href=True) :
        if 'b.tech' in urllib.parse.unquote(a['href']).lower() or 'btech' in urllib.parse.unquote(a['href']).lower() and datef(urllib.parse.unquote(a['href'])[5:11]) in date_list :
            print(a)
            notice_date[urllib.parse.unquote(a['href']).split('/')[-1]] = {'http://ggsipu.ac.in/ExamResults/'+ a['href'] : datef(urllib.parse.unquote(a['href'])[5:11])}

    return notice_date