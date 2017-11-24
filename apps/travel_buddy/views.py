# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q


def index(request):
    return render(request, 'travel_buddy/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], email = request.POST['email'], birthday = request.POST['birthday'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")        
    return redirect('/travels')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/travels')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def users(request, user_id):
    context={"user": User.objects.get(id=user_id)}
    return render(request, 'travel_buddy/travels.html', context)

def travels(request):
    return render (request, 'travel_buddy/travels.html')

def destination_list(request):
    user = User.objects.get(id =request.session['id'])
    context={
        'user':user,
        'destination': Destination.objects.filter(created_by=user),
        'joined_by_user': Destination.objects.filter(joined = user),
        'joined_by_others': Destination.objects.exclude(joined = user),
        'going': Destination.objects.filter(joined=user),
        'created_by_others': Destination.objects.all().exclude(joined__id=request.session['id']),
        'created_by': User.objects.get(id =request.session['id'])
    }
    return render(request, 'travel_buddy/travels.html', context)

def destination(request, destination_id):
    context = {
    'destination': Destination.objects.get(id = destination_id)  
    }
    return render(request, 'travel_buddy/destination.html', context)

def add(request):
    return render (request, 'travel_buddy/add.html')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
        messages.success(request, "You have logged out")
    return redirect('/')

def create(request):
    print
    error_2 = Destination.objects.destination(request.POST)
    if 'errors' in error_2:
        for error in error_2:
            print error_2[error]
            messages.error(request, error_2[error])
        return redirect('travel_buddy/add')
    else:
        user = User.objects.get(id =request.session['id'])
        destination1 = Destination.objects.create(destination = request.POST['destination'], description = request.POST['description'], date_from =request.POST['date_from'], date_to = request.POST['date_to'], created_by = user)
        destination1.joined.add(user)
        destination1.save()
        messages.error(request, "You have successfully added an destination")        
        return redirect('/travels')

def join(request, destination_id):
    destination = Destination.objects.get(id = destination_id)
    user = User.objects.get(id =request.session['id'])
    destination.joined.add(user)
    return redirect('/travels')


