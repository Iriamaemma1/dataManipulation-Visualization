import csv
#from django.urls import reverse
import logging
import statistics
from email.mime import image
from multiprocessing import context
from sqlite3 import Row
from tkinter import Image
from urllib import request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from django.conf import settings
#from .forms import CsvBulkUploadForm
from django.conf.urls.static import static
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
#dataset=pd.read_csv("test.csv")
from scipy.stats import norm

#%matplotlib inline
import datavisual.static.datavisual.csvfiles as csv

from .forms import CsvForm
from .models import Csv

# Create your views here.
read= None
columns= None
dataset= None
read=Csv.objects.last().file_name.path or None
#dataset=pd.read_csv(Csv.objects.get(activated=True).file_name.path)
if read is not None:
   dataset=pd.read_csv(read)

   columns=dataset.columns.to_list() 

def home(request):
    if columns is not None:
      context={
        'columns':columns
    }
    return render(request,'datavisual/index.html',context)
 

def histogram(request):
    upload_file_view(request)
    fig, ax = plt.subplots(1,2)
    ax[0].hist(x=dataset[xaxis], bins = 1000)
    #fig.show()
    #(x=dataset['Rating'], bins = 1000)
    ax[1].hist(x=dataset[yaxis], bins = 1000)
    df=plt.show()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View Histogram here</h1> ")
    
    
    #return HttpResponse("<h1>{{dataset.info}}</h1> ")
    

def scatter(request):
    upload_file_view(request)
    plt.scatter(x=dataset[xaxis], y=dataset[yaxis])
    graph=plt.show()

    content2={
       'graph': graph, 
    }
    #return HttpResponse("<h1>View scatter plot here</h1>")
    return render(request, 'datavisual/scatter.html', content2)

def first5(request):
    df=dataset.head().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View first5 here</h1>")

def last5(request):
    df=dataset.tail().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View last5 here</h1>")


def modelStats(request):
    stats=dataset.describe().to_html()
    content2={
        'stats':stats
    }
    return render(request, 'datavisual/stats.html', content2) 

def normalDistCurve(request):
    upload_file_view(request)
    mean = statistics.mean(dataset[xaxis])
    sd = statistics.stdev(dataset[xaxis])
  
    plt.plot(dataset[xaxis], norm.pdf(dataset[xaxis], mean, sd))
    df=plt.show()
    #df=sns.displot(dataset['Revenue (Millions)'])
    
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View normal distribution curve here</h1>")

def description(request):
    df=dataset.head(dataset.shape[0]).to_html()
    #df=dataset.sort_values(by='Rank',ascending=True).value_counts(sort=True,ascending=True).to_frame().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View description here</h1>")          

def upload_file_view(request):
    if request.method=="POST":
        global xaxis
        global yaxis
        xaxis=request.POST.get('xaxis','default')
        yaxis=request.POST.get('yaxis','default')
    
    error_message = None
    success_message = None
    #Csv.objects.delete()
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        success_message= "Uploaded sucessfully"
        #obj = Csv.objects.get(activated=False)
        #obj.activated=True
        
        #with open(obj.file_name.path, 'r') as f:
             #reader = csv.reader(f)
        # obj.activated=True
        # obj.save()    
        # success_message= "Uploaded sucessfully"
        # try:
        #     obj = Csv.objects.get(activated=False)
        #     with open(obj.file_name.path, 'r') as f:
        #         reader = csv.reader(f)

        #         for row in reader:
        #             row = "".join(row)
        #             row = row.replace(";", " ")
        #             row = row.split()
        #             user = User.objects.get(id=row[3])
        #             prod, _ = Product.objects.get_or_create(name=row[0])
        #             Purchase.objects.create(
        #                 product=prod,
        #                 price = int(row[2]),
        #                 quantity = int(row[1]),
        #                 salesman = user,
        #                 date = row[4]+ " "+ row[5]
        #             )

        #     obj.activated=True
        #     obj.save()
        #     success_message= "Uploaded sucessfully"
        # except:
        #     error_message = "Ups. Something went wrong...."
    # else:
    #     error_message = "Ups. Something went wrong...."
    #if columns is not None:
    context = {
        'form': form,
        'success_message': success_message,
        'columns':columns
        #'error_message': error_message,
        #'uploaded_file_url':f,
    }
    return render(request, 'datavisual/index.html',context)


# def upload_csv(request):
# 	data = {}
# 	if "GET" == request.method:
# 		return render(request, "datavisual/upload_csv.html", data)
#     # if not GET, then proceed
# 	try:
# 		csv_file = request.FILES["csv_file"]
# 		if not csv_file.name.endswith('.csv'):
# 			messages.error(request,'File is not CSV type')
# 			return HttpResponseRedirect(reverse("datavisual:upload_csv"))
#         #if file is too large, return
# 		if csv_file.multiple_chunks():
# 			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
# 			return HttpResponseRedirect(reverse("datavisual:upload_csv"))

# 		file_data = csv_file.read().decode("utf-8")		

# 		lines = file_data.split("\n")
# 		#loop over the lines and save them in db. If error , store as string and then display
# 		for line in lines:						
# 			fields = line.split(",")
# 			data_dict = {}
# 			data_dict["name"] = fields[0]
# 			data_dict["start_date_time"] = fields[1]
# 			data_dict["end_date_time"] = fields[2]
# 			data_dict["notes"] = fields[3]
# 			try:
# 				form = file_data(data_dict)
# 				if form.is_valid():
# 					form.save()					
# 				else:
# 					logging.getLogger("error_logger").error(form.errors.as_json())												
# 			except Exception as e:
# 				logging.getLogger("error_logger").error(repr(e))					
# 				pass

# 	except Exception as e:
# 		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
# 		messages.error(request,"Unable to upload file. "+repr(e))

# 	return HttpResponseRedirect(reverse("datavisual:upload_csv"))

# def upload_csv(request):
#   if request.method == 'GET':
#     form = CsvBulkUploadForm()
#     return render(request, 'datavisual/upload_csv.html', {'form':form})

#   # If not GET method then proceed
#   try:
#     form = CsvBulkUploadForm(data=request.POST, files=request.FILES)
#     if form.is_valid():
#       csv_file = form.cleaned_data['csv_file']
#     if not csv_file.name.endswith('.csv'):
#       messages.error(request, 'File is not CSV type')
#       return redirect('datavisual:upload_csv')
#     # If file is too large
#     if csv_file.multiple_chunks():
#       messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
#       return redirect('datavisual:upload_csv')
    
#     file_data = csv_file.read().decode('utf-8')
#     lines = file_data.split('\n')

#     # loop over the lines and save them in db. If error, store as string and then display
#     for line in lines:
#       fields = line.split(',')
#       data_dict = {}
#       print(data_dict)
#       try:
#         form = CsvBulkUploadForm(data_dict)
#         if form.is_valid():
#           form.save()
#         else:
#           logging.getLogger('error_logger').error(form.errors.as_json())
#       except Exception as e:
#         logging.getLogger('error_logger').error(form.errors.as_json())
#         pass
#   except Exception as e:
#     logging.getLogger('error_logger').error('Unable to upload file. ' + repr(e))
#     messages.error(request, 'Unable to upload file. ' + repr(e))
#   return redirect('datavisual:upload_csv')



# def upload_csv(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         fs = FileSystemStorage()
#         csv_file = fs.save(csv_file.name, csv_file)
#         uploaded_file_url = fs.url(csv_file)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'core/simple_upload.html')
