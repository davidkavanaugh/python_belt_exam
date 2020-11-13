from django.db import models
from users.models import User
from datetime import datetime
from datetime import date


class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not len(postData['destination']) > 0:
            errors['destination'] = "Please enter a destination"
        if not len(postData['plan']) > 2:
            errors['plan'] = "Please enter a valid plan"
        try:
            datetime.strptime(
                postData["start_date"], '%m/%d/%Y')
            print("Date is valid.")
        except ValueError:
            errors['start_date'] = "Please enter a valid start date"
        try:
            datetime.strptime(
                postData["end_date"], '%m/%d/%Y')
            print("Date is valid.")
        except ValueError:
            errors['end_date'] = "Please enter a valid end date"
        try:
            if not datetime.now() < datetime.strptime(postData["start_date"], '%m/%d/%Y'):
                errors['start_date'] = "Start date must be in the future"
        except ValueError:
            print(ValueError)
        try:
            if datetime.strptime(postData["start_date"], '%m/%d/%Y') > datetime.strptime(postData["end_date"], '%m/%d/%Y'):
                errors['date'] = "Start date must come before end date"
        except ValueError:
            print(ValueError)
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.ForeignKey(
        User, related_name="trips_created", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
