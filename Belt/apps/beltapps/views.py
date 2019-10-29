from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'frontpage.html')


def register_process(request):

    print(request.POST)

    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        print(password)
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        User.objects.create(
            email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_pw)

        messages.success(request, "Registration Successful")
        return redirect('/')


def login_process(request):
   
    forminfo = request.POST
    print(forminfo)
    user = User.objects.filter(email = request.POST['email'])
    print(user)
    if user:
        logged_user = user[0]
        
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id

            # print('successful login', request.session['user_id'])
            return redirect('/dashboard')
        
    return redirect ('/')
 

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        print(f"ppppppooooooooo----->{ user.trips_created.all()}")

        context = {
           'user' : user,
           'trips' : user.trips_created.all()
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "You must login!")
        return render(request, '/dashboard', context)
def logout(request):
    request.session.clear()
    return redirect('/')

def newtrip(request):
    #user_id=request.session['user_id']
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user
    }

    return render(request,'newtrip.html', context)

def process_new(request):
    print("creating a new trip", request.POST)
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.create(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        plan = request.POST['plan'],
        created_by = user
    )
    return redirect('/dashboard')

def viewtrip(request,trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip' : trip,
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'viewtrip.html', context)
def remove(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()

    return redirect('/dashboard')
    
def edittrip(request,trip_id):
    user = User.objects.get(id = request.session['user_id'])
    trip = Trip.objects.get(id = trip_id)
    context = {
        'trip' : trip,
        'user' : user
    }
    return render(request, 'edittrip.html', context)

def update(request):
    print(request.POST)
    user=User.objects.get(id=request.session['user_id'])
    trip=Trip.objects.get(id=request.POST['trip_id'])
    trip.destination=request.POST['destination']
    trip.start_date=request.POST['start_date']
    trip.end_date=request.POST['end_date']
    trip.plan=request.POST['plan']
    created_by = user
    trip.save()
    return redirect ('/dashboard')
    
def edit(request):
    print(f"ppppppooooooooo------------------------>", request.POST)
    user = User.objects.get(id=request.session['user_id'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, "Please make sure all fileds are filled in correctly")
        return redirect(f'/trips/edit/{trip_id}')
    else:
        trip = Trip.objects.get(id=request.session['trip_id'])
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()  

    return redirect ('/dashboard')

        