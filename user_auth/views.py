# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm
from .forms import LoginForm

# Create your views here.
def register(request):
     
    if request.method == 'POST':
        response = HttpResponse()
        response.write("<h1>Thanks for registering</h1></br>")
        response.write("Your username: " + request.POST['username'] + "</br>")
        response.write("Your email: " + request.POST['email'] + "</br>")
        return response 
  
    registerForm = RegisterForm() 
    return render(request, 'user_auth/register.html', {'form':registerForm})

def loginView(request):
    username = "Wrong username or password"

    if request.method == "POST":
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            if MyLoginForm.cleaned_data['username'] == 'admin':
                if MyLoginForm.cleaned_data['password'] == '123':
                    username = MyLoginForm.cleaned_data['username']
                    request.session['username'] = username
                    request.session.set_expiry(15);
    else:
        MyLoginForm = LoginForm()

    return render(request,'loggedin.html',{'username':username})

def formView(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'loggedin.html', {'username':username})
    else:
        return render(request, 'login.html', {})
  
def logoutView(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponse("Good bye!")
    
        
