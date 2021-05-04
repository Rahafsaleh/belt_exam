from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "please check your first name, it most be more than 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "please check your last name, it most be more than 2 characters"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "please inter a valid email"
        if len(post_data['password']) < 8:
            errors['password'] = "please check your Password, it most be more than 2 characters"
        if post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Passwords does not match"
        print("reached the validator for register")
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) > 0:
            errors['not_unique'] = "Please change the Email, it is already exists"
        return errors


    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Please inter a valid email"
        if len(post_data['password']) < 8:
            errors['password'] = "please check your Password, it most be more than 2 characters"
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email2'] = "Email does not exists"
        elif not bcrypt.checkpw(post_data['password'].encode(), user_list[0].password.encode()):
            errors['match'] = "Wrong Password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class TripManager(models.Manager):
    def trip_validator(self, postdata):
        errors={}
        today = datetime.now()
        start_date = datetime.strptime(postdata['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(postdata['end_date'], '%Y-%m-%d')


        if len(postdata['destination'])<3:
            errors['destination']=" Your destination must be at least 3 characters long"
        if len(postdata['plan'])<3:
            errors['plan']=" Your plan must be at least 3 characters long!"
        
        if postdata['start_date'] == '':
            errors['start_date'] = "Please enter a start date!"
        elif start_date <= today :
            errors['start_date'] = "Start date must be in the future!"
        if postdata['end_date'] == '':
            errors['end_date'] = "Please enter an end date!"
        elif end_date < start_date :
            errors['end_date'] = "Please make sure that the end date is after the start date!"
        
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=75)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    planed_by = models.ForeignKey(User,related_name="user_trip",on_delete=models.CASCADE)
    join = models.ManyToManyField(User, related_name="join_trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()