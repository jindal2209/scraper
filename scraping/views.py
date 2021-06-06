from django.http import HttpResponse
from django.shortcuts import render
from . import webscraping,pdftoexcelOLD
import requests
import urllib.parse
import time

## progress bar printer just for fun and interactive visualisation
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def index(request):
	return render(request, "scraping\home.html")

def check(request):
	link = request.GET['link']
	date1 = request.GET["initial_date"]
	date2 = request.GET["final_date"]
	notice_date = webscraping.scraping(link,date1,date2)

	return render(request,"scraping\list.html",{"list":notice_date,'files': len(notice_date)})


coun = 0

def download(request):
	
	l = 2*len(request.GET.getlist('value_checkbox'))
	global coun
	coun = 0
	printProgressBar(0, l, prefix = 'Downloading:', suffix = 'Complete', length = 50)

	for i in request.GET.getlist("value_checkbox"):
		printProgressBar(coun, l, prefix = 'Downloading:', suffix = 'Complete', length = 50)
		
		i = urllib.parse.unquote(i)
		myfile = requests.get(i, allow_redirects=True)
		filename = i.split('/')[-1]
		with open('generated_pdfs\\' + filename, 'wb') as f :
			f.write(myfile.content)
		f.close()
		coun+=1

		printProgressBar(coun, l, prefix = 'Parsing File:', suffix = 'Complete', length = 50)
		pdftoexcelOLD.CreateExcel(path='generated_pdfs\\'+filename , filename=filename)
		
		coun+=1

	print("{no} files parsed successfully".format(no=len(request.GET.getlist('value_checkbox'))))
	return HttpResponse("Downloaded {no} files ".format(no=len(request.GET.getlist('value_checkbox'))))

