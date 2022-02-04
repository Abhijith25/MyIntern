
import json
from django.shortcuts import render, redirect
import requests
from django.urls import reverse
from django.contrib import messages

username = ""
# Create your views here.

posts = [
    {
        'author': 'VSA',
        'title': 'My Day 3',
        'content': 'You are never well dressed without a smile ♥',
        'date_posted': 'January 18, 2022'
    },
    {
        'author': 'Abhijith',
        'title': 'My Day 2',
        'content': 'Each day is a new Beginning and I begin today with a smile.',
        'date_posted': 'January 17, 2022'
    },
    {
        'author': 'Abhijith',
        'title': 'My Day 1',
        'content': 'Hardwork beats talent when talent doesnt work hard',
        'date_posted': 'January 16, 2022'
    }
    
]


def home(request):

    res = requests.get('http://localhost:5000/getPosts')
    post_data = res.json()

    context = {
        'posts': post_data
    }
    return render(request,'myapp/home.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {
            'username':username,
            'email':email,
            'password':password
        }

        api_url = 'http://localhost:5000/register'

        r = requests.post(url=api_url, json=data)

        if r.status_code == 200:
            messages.success(request, "User registered successfully")
            args = {}
            usr = username
            args['usr'] = usr
            return redirect('/')
            
        
        else:
            for key, value in r.json().items():
                if(key == 'status' and value == 'User Already exists'):
                    msg = value
                    messages.error(request,msg)
                    return redirect('myapp-login')
                    
    return render(request,'myapp/register.html')

def login(request):

    if request.method == 'POST':
        
        usrmail = request.POST.get('usrmail')
        password = request.POST.get('password')

        data = {
            'usrmail':usrmail,
            'password':password
        }

        api_url = 'http://localhost:5000/login'

        r = requests.post(url=api_url, json=data)

        if r.status_code == 200:
            global username
            request.session['usrmail'] = usrmail
            print(request.session['usrmail'])
            username = request.session['usrmail']
            messages.success(request, "Welcome "+username)
            
            # return redirect('myapp-home')
            context = {'username': username,'posts': posts}
            return render(request, "myapp/home.html", context)
            
            
            
        
        else:
            for key, value in r.json().items():
                if(key == 'status'):
                    msg = value
                    messages.error(request, msg)
                    return redirect('myapp-login')

    return render(request,'myapp/login.html')

def about(request):
    return render(request,'myapp/about.html')

def logout(request):
    request.session['usrmail'] = ""
    return redirect('myapp-login')

def addposts(request):
    if request.session['usrmail'] != "":
        if request.method == 'POST':
            post_title = request.POST.get('post_title')
            post_author = request.POST.get('post_author')
            post_content = request.POST.get('post_content')

            print(post_title+"\n"+ post_author+"\n"+post_content)

            data = {
                'post_title':post_title,
                'post_author':post_author,
                'post_content':post_content
            }

            api_url = 'http://localhost:5000/addPosts'

            r = requests.post(url=api_url, json=data)

            if r.status_code == 200:
                messages.success(request, "Post created")
                return redirect('/')
            else:
                messages.error(request, "Couldn't post")
                return render(request, )


            
        
        return render(request,'myapp/addposts.html', {'username': request.session['usrmail']})
    else:
        return render(request,'myapp/login.html')

