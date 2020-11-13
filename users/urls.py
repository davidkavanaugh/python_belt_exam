from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_user),
    path('get', views.get_user)
]
