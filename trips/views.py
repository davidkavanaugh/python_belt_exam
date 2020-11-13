from django.shortcuts import render, redirect
from users.models import User
from .models import Trip
from django.contrib import messages
from datetime import datetime


def index(request):
    return redirect('/')


def new_trip(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user
    }
    return render(request, "new_trip.html", context)


def create_trip(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="trip")
        return redirect('/trips/new')
    else:
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(
            destination=request.POST['destination'],
            start_date=datetime.strptime(
                request.POST["start_date"], '%m/%d/%Y'),
            end_date=datetime.strptime(
                request.POST["end_date"], '%m/%d/%Y'),
            plan=request.POST['plan'],
            created_by=user
        )
        trip.attendees.add(user)
        trip.save()
        return redirect('/')


def get_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    context = {
        "user": user,
        "trip": trip
    }

    return render(request, "trip.html", context)


def edit_trip(request, trip_id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.start_date = trip.start_date.strftime('%m/%d/%Y')
    trip.end_date = trip.end_date.strftime('%m/%d/%Y')
    context = {
        "user": user,
        "trip": trip
    }
    return render(request, "edit_trip.html", context)


def update_trip(request, trip_id):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="trip")
        return redirect(f'/trips/edit/{trip_id}')
    else:
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.start_date = datetime.strptime(
            request.POST["start_date"], '%m/%d/%Y')
        trip.end_date = datetime.strptime(
            request.POST["end_date"], '%m/%d/%Y')
        trip.plan = request.POST['plan']
        trip.save()
        return redirect('/')


def add_trip(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.attendees.add(user)
    return redirect('/')


def remove_trip(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.attendees.remove(user)
    return redirect('/')


def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/')
