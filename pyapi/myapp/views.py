from django.shortcuts import render
from django.http import HttpResponse, response
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

import json
from django.contrib.auth.models import User
from myapp.models import Exercise
# Create your views here.

def index(request):
    response=json.dumps([{}])
    return HttpResponse(response,content_type= 'text/json')

@csrf_exempt
def add_user(request):
    if request.method=='POST':
        print(request.body)
        print(request.body.decode('utf-8'))
        payload = json.loads(request.body.decode('utf-8'))
        user_name=payload['username']
        user_password=payload['password']
        user_email=payload['email']

        
        try:
            user = User.objects.create_user(user_name, user_email, user_password)
            user.save()
            response= json.dumps([{'Success': str(True)}])
        except Exception as e:
            response= json.dumps([{'Error': e}])
    return HttpResponse(response,content_type= 'text/json')

@csrf_exempt
def add_exercise(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            print(request.body.decode('utf-8'))
            payload = json.loads(request.body.decode('utf-8'))
            name=payload['name']
            totalHint=payload['totalHint']
            foundHints=payload['foundHint']
            time= payload['time']
            exercise = Exercise(name=name,userId=request.user,hintsTotal=int(totalHint),hintsFound=int(foundHints),time=float(time))
            try:
                exercise.save()
                response= json.dumps([{'exerciseAdded': str(True)}])
            except Exception as e:
                response= json.dumps([{'Error': e}])
        else:
            response= json.dumps([{'authenticated': str(False)}])

        return HttpResponse(response,content_type= 'text/json')

@csrf_exempt
def logout_view(request):
    logout(request)


@csrf_exempt
def get_user(request):
    if request.method=='GET':
        uname=request.GET.get('username')
        upassword=request.GET.get('password')
        print(uname)
        print(upassword)
        user = authenticate(username=uname, password=upassword)

        if user is not None:
            login(request, user)
            response= json.dumps([{'Success': str(True) }])


        else:
            response= json.dumps([{'Error': "could not find user"}])


    return HttpResponse(response,content_type= 'text/json')

@csrf_exempt
def get_exercises(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            try:
                all =Exercise.objects.all().filter(userId=request.user)
                returned=[]
                for e in all:
                    expanded= [e.name,e.hintsTotal,e.hintsFound,e.time]
                    returned.append(expanded)

                response= json.dumps([{'Exercises': str(returned)}])
            except Exception as e:
                response= json.dumps([{'Error': e}])
            
        else:
            response= json.dumps([{'authenticated': str(False)}])

        return HttpResponse(response,content_type= 'text/json')

@csrf_exempt
def get_exerciseType(request,e_name):
    if request.method=='GET':
        if request.user.is_authenticated:
            try:
                all =Exercise.objects.all().filter(userId=request.user,name=e_name)
                returned=[]
                for e in all:
                    expanded= [e.name,e.hintsTotal,e.hintsFound,e.time]
                    returned.append(expanded)

                response= json.dumps([{'Exercises': str(returned)}])
            except Exception as e:
                response= json.dumps([{'Error': e}])
        else:
            response= json.dumps([{'authenticated': str(False)}])

        return HttpResponse(response,content_type= 'text/json')