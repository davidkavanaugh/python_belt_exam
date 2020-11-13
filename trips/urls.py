from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.new_trip),
    path('create', views.create_trip),
    path('<int:trip_id>', views.get_trip),
    path('edit/<int:trip_id>', views.edit_trip),
    path('update/<int:trip_id>', views.update_trip),
    path('delete/<int:trip_id>', views.delete_trip),
    path('add/<int:trip_id>', views.add_trip),
    path('remove/<int:trip_id>', views.remove_trip)
]
