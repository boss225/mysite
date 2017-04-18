# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from .forms import UploadFileForm

# Create your views here.
def fileUploaderView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload(request.POST['title'],request.FILES['file'])
            return HttpResponse("<h2>File uploaded successful!</h2>")
        else:
            return HttpResponse("<h2>File uploaded not successful!</h2>")
 
    form = UploadFileForm()
    return render(request, 'fileUploaderTemplate.html', {'form':form})
  
def upload(t,f): 
    file = open('upload/files/'+t, 'wb+') 
    for chunk in f.chunks():
        file.write(chunk)