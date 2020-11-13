from django.shortcuts import render, redirect
from users.models import User


def index(request):
    if not 'user_id' in request.session:
        return redirect('/sign-in')
    else:
        context = {
            "user": User.objects.get(id=request.session["user_id"]),
        }

        return render(request, "index.html", context)


def sign_up(request):
    if 'user_id' in request.session:
        return redirect('/')
    else:
        return render(request, "sign-up.html")


def sign_in(request):
    if 'user_id' in request.session:
        return render('/')
    else:
        return render(request, "sign-in.html")


def log_out(request):
    del request.session['user_id']
    return redirect('/')
