from django.shortcuts import render, redirect
from users.models import User
from trips.models import Trip


def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, "index.html")


def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    other_trips = Trip.objects.all()
    context = {
        "user": user,
        "trips": user.trips.all()
    }
    for trip in other_trips:
        if user in trip.attendees.all():
            trip.joined = False
    context['other_trips'] = other_trips
    return render(request, "dashboard.html", context)


def log_out(request):
    del request.session['user_id']
    return redirect('/')
