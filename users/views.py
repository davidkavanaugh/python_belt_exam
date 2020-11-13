from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt


def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sign-up')
    else:
        pw_hashed = bcrypt.hashpw(
            request.POST['password_1'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hashed
        )
        messages.success(request, "Registration successful!")
        return redirect('/sign-in')


def get_user(request):
    if len(request.POST['email']) == 0 or len(request.POST['password']) == 0:
        messages.error(request, "Please enter an email and password")
        return redirect('/sign-in')
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            request.session['user_id'] = user[0].id
            return redirect('/')
        else:
            messages.error(request, "Email / Password incorrect")
    else:
        messages.error(request, "User not found")
    return redirect('/sign-in')
