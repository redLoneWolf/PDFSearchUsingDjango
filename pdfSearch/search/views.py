from django.shortcuts import render
import os
import fitz
import time
from django.conf import settings
from .models import Pics,Search

file_paths=[]

def get_save_path(fname,page,timestamp):
    path=os.path.join(settings.MEDIA_ROOT,"temp",str(timestamp))
    os.makedirs(path, exist_ok=True)
    return "{path}/{fname}-{page}.{ext}".format(path=path,fname=fname,page=page,ext="png")

def get_image_url(fname,page,timestamp):
    return "media/temp/{timestamp}/{fname}-{page}.{ext}".format(timestamp=timestamp,fname=fname,page=page,ext="png")
    
def get_pdf_paths():
    return os.path.join(settings.MEDIA_ROOT, "pdfs")


if os.path.isdir(get_pdf_paths()):
    for filename in os.listdir(get_pdf_paths()):
        if filename.endswith(".pdf"): 
            file_paths.append(os.path.join(get_pdf_paths(), filename))
else:      
    print()
    print("Warning ! Save your pdf files in ",get_pdf_paths())
    print()
    
    
        
def searchAll(text):


    searchq = Search.objects.create(keyText=text)

    qs = []
    pgs=[]
    found_in_files = []

    if len(file_paths)<=0:
        print()
        print("Warning ! Save your pdf files in ",get_pdf_paths())
        print()

    for fname in file_paths:
        doc = fitz.open(fname)
        for page in doc:
            text_instances = page.searchFor(text)

            if len(text_instances)>0:
                pgs.append(page.number)
                
                head, tail = os.path.split(fname)
                filename = os.path.splitext(tail)[0]
                pdfPath = "media/pdfs/{file_name}".format(file_name=tail)
                # pdfs.append(pdfPath)

                found_in_files.append(filename)
                # print("f",pdfs)

                for inst in text_instances:
                    highlight = page.addHighlightAnnot(inst)
                    highlight.update()
                

                pix = page.get_pixmap(alpha = False) 
                t =str(int(time.time()))

                imageFilePath = get_save_path(filename,page.number, t)
                imageUrl = get_image_url(filename,page.number,t)
                # image_urls.append(imageUrl)

                pix.save(imageFilePath)

                qs.append(Pics.objects.create(pdf=pdfPath,search=searchq,image=imageUrl,page=page.number))
                # print(qs)
    return qs
             
            

def home(request):
    
    ctx = {}

    if "search" in request.GET:
        search = request.GET.get('search')
        print("search")
        qs = searchAll(search)
        ctx['qs']=qs
    
    elif "historyq" in request.GET:
        print("didnt search")
        history = request.GET.get('historyq')
        qs = Pics.objects.filter(search__keyText=history)
        ctx['qs']=qs
    


    his = Search.objects.all()
    ctx['history']=his
  
    return render(request, "index.html",context=ctx)


def detail(request):

    return render(request, "viewer.html")


