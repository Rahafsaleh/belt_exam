from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import date


def index(request):
    if 'uid' in request.session:
        return redirect("/dashboard")
    context = {
        'today': date.today()
    }
    return render(request, "index.html", context)


def welcome(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['uid'])
    }
    return render(request, "dashboard.html", context)


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  # create the hash
        print(pw_hash)
       
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['uid'] = new_user.id
        return redirect("/dashboard") 


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['uid'] = logged_user.id
        return redirect('/dashboard')    
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    context = {
        "this_user": User.objects.get(id=request.session['uid']),
        "all_tripes": Trip.objects.all(),
        "userplan_sorted":User.objects.get(id=request.session['uid']).user_trip.all().order_by('-id'),
        "other_trip" : Trip.objects.exclude(planed_by=User.objects.get(id=request.session['uid'])).exclude(join=User.objects.get(id=request.session['uid'])),
        "join_trip" : Trip.objects.filter(join=User.objects.get(id=request.session['uid']))
    }
    return render(request,"dashboard.html", context)

def create_trip(request):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("found an errors")
            return redirect("/dashboard/new_trip")
        
        Trip.objects.create(
            destination = request.POST['destination'],
            plan = request.POST['plan'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            planed_by = User.objects.get(id=request.session['uid'])
        )
    return redirect("/dashboard")

def new_trip(request):
    context = {
        "this_user": User.objects.get(id=request.session['uid']),
        "all_tripes": Trip.objects.all(),
    }
    return render(request,"new.html", context)

def add_trip(request, id):
    this_user = User,objects.get(id=request.session['uid'])
    this_user.user_trip.add(Trip.objects.get(id=id))
    return redirect("/dashboard")

def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect("/dashboard")

def edit(request, id):
    context = {
        "this_user": User.objects.get(id=request.session['uid']),
        "trip": Trip.objects.get(id=id)
    }
    return render(request,"edit.html", context)

def update_trip(request, id):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print(" found errors")
            return redirect(f"/dashboard/edit/{id}")
           
        trip = Trip.objects.get(id=id)
        trip.destination = request.POST['destination']
        trip.plan = request.POST['plan']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.save()
    return redirect("/dashboard")

def show_trip(request, id):
    context = {
        "this_user": User.objects.get(id=request.session['uid']),
        "join_trip" : Trip.objects.filter(join=User.objects.get(id=request.session['uid'])),
        "trip": Trip.objects.get(id=id)
    }
    return render(request,"show.html", context)

def join(request, id):
    this_user=User.objects.get(id=request.session['uid'])
    this_trip=Trip.objects.get(id=id)
    this_trip.join.add(this_user)
    return redirect("/dashboard")

def cancel(request, id):
    this_trip=Trip.objects.get(id=id)
    this_user=User.objects.get(id=request.session['uid'])
    this_trip.join.remove(this_user)
    return redirect("/dashboard")

