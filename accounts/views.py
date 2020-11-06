from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from . apps import *
from random import randint
import string
import random
from pages.models import Address
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('login')
    return render (request,'pages/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        Firstname = request.POST['firstname']
        Lastname = request.POST['lastname']
        Username = request.POST['username']
        Email = request.POST['email']
        # Password = request.POST['password']
        # Confirm_password = request.POST['confrim_password']
        print('-----------4')

        if User.objects.filter(username=Username).exists():
            print('-----------5')
            return redirect('register')
        else:
            if User.objects.filter(email=Email).exists():
                print('-----------1')
                return redirect('register')
            else:
                print('-----------2')
                letters = string.ascii_letters + string.digits + string.punctuation
                Password = ''.join(random.choice(letters) for i in range(8))
                user = User.objects.create_user(first_name=Firstname,last_name=Lastname,email=Email,password=Password,username=Username)
                email_subject = "Django Subject"
                sendmail(email_subject, 'mail_template', Email, {'name': Username, 'Password': Password})
                auth.login(request,user)
                # return redirect('home')
                user.save()
                print('-----------3')
                return redirect('login')
    return render(request,'pages/register.html') 

def userDetail(request):
    user_detail = User.objects.filter(username=request.user.username)
    user_address = Address.objects.filter(user=request.user.id)
    print(user_address)
    context = {
        'user_detail':user_detail,
        'user_address':user_address,
    }
    return render(request,'pages/user.html',context)              

