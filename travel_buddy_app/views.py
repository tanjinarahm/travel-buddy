from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import *
import bcrypt

def index(request):
    all_trips = Travel.objects.all()

    context = {
        "others": all_trips
    }

    return render(request, "travels.html", context)

def signup(request):
    context = {
        "signup": True
    }
    return render(request, "login_reg.html", context)

def login(request):
    return render(request, "login_reg.html")

def travels(request):
    if 'loggedinUser' in request.session:
            
        current_user = User.objects.get(id=request.session['loggedinUser'])
        all_trips = Travel.objects.exclude(creator=current_user)

        all_trips = all_trips.exclude(trip_member=current_user)

        length = len(current_user.joined_trip.all())

        context = {
            "user": current_user,
            "travels": current_user.joined_trip.all(),
            "others": all_trips,
            "logged_in": True,
            "trip_count": length
        }
    else: 
        all_trips = Travel.objects.all()
        context = {
            "logged_in": False,
             "others": all_trips
        }
    return render(request, "travels.html", context)

    # The eedeeit way
    # if 'loggedinUser' in request.session:
    #     context = {
    #         "user": User.objects.get(id=request.session['loggedinUser']),
    #         "travels" : Travel.objects.filter(trip_member = request.session['loggedinUser']),
    #         "others": Travel.objects.exclude(trip_member = request.session['loggedinUser']),
    #         "logged_in": True
    #     }
    #     return render(request, "travels.html", context)
    # else:
    #     return redirect("/")

def registerUser(request, method = "POST"):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        request.session['err'] = "register"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')

    else:
        passwordFromForm = request.POST['password']
        hashedPass = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
        new_user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashedPass.decode())
        request.session["loggedinUser"] = new_user.id 
    return redirect("/travels")

def loginUser(request, method = "POST"):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        request.session['err'] = "login"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')

    else:
        username = request.POST['username']
        user = User.objects.filter(username = request.POST['username'])
        current = user[0]
        if user:
            current = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), current.password.encode()):
                request.session["loggedinUser"] = current.id
    return redirect('/travels')

def addTravel(request):
    return render(request, "addTravels.html")


def add(request, method = "POST"):
    errors = Travel.objects.travel_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        current_user = User.objects.get(id = request.session["loggedinUser"])
        plan = Travel.objects.create(destination=request.POST['destination'],description=request.POST['description'], start_date=request.POST['start_date'],end_date = request.POST['end_date'], creator= current_user)
        plan.trip_member.add(User.objects.get(id = request.session["loggedinUser"]))
        plan.save()
    return redirect("/travels")


def viewTrip(request, travel_id):
    travel_to_show = Travel.objects.get(id = travel_id)
    # current_user = User.objects.get(id = request.session["loggedinUser"])
    context ={
        "user": User.objects.get(id = request.session["loggedinUser"]),
        "travel": travel_to_show,
        "others": User.objects.filter(joined_trip = travel_id)
    }
    return render(request, "viewTrip.html", context)


def join(request, travel_id):
    travel = Travel.objects.get(id = travel_id)
    travel.trip_member.add(User.objects.get(id = request.session["loggedinUser"]))
    return redirect('/travels')


def logout(request):
    del request.session['loggedinUser']
    return redirect("/")