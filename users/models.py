from django.db import models
import re


class SignUpManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&/])[A-Za-z\d$@$!%*?&]{8,}")
        if not FIRST_NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Valid first name required"
        if not LAST_NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Valid last name required"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Valid email required"
        if not PASSWORD_REGEX.match(postData["password_1"]):
            errors['password'] = "Password too weak"
        if postData['password_1'] != postData['password_2']:
            errors['password'] = "Passwords must match"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['user_exists'] = "User already exists"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default="")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SignUpManager()
