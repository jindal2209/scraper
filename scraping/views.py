from django.http import HttpResponse
from django.shortcuts import render
from . import webscraping
import requests
import urllib.parse
# import FinalMArch2020XLSCreator

def index(request):
    return render(request, "scraping\home.html")

def check(request):
    link = request.GET['link']
    date1 = request.GET["initial_date"]
    date2 = request.GET["final_date"]
    notice_date = webscraping.scraping(link,date1,date2)
    
    return render(request,"scraping\list.html",{"list":notice_date,'files': len(notice_date)})

def download(request):
    for i in request.GET.getlist("value_checkbox"):
        i = urllib.parse.unquote(i)
        myfile = requests.get(i, allow_redirects=True)
        with open(i.split('/')[-1], 'wb') as f :
            f.write(myfile.content)

    return HttpResponse("Downloaded")