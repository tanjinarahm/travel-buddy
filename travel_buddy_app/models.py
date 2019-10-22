from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re

class User_Manager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0 and len(postData ['username']) == 0 and len(postData['password']) == 0 and len(postData['confirm_pw']) == 0:
            errors['name'] = "Please fill out the form"
        else:
            if len(postData['name']) < 4:
                errors["name"] = "Name should at least be 3 characters"
            if len(postData ['username']) < 4:
                errors["username"] = "Username should at least be 3 characters"
            user = User.objects.filter(username = postData['username'])
            if user:
                errors["username"] = "Username is already in use"
            if len(postData['password']) < 8:
                errors["password"] = "Password at least be 8 characters"
            else:
                if postData["password"] != postData["confirm_pw"]:
                    errors["confirm_pw"] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['username']) == 0 and len(postData['password']) == 0:
            errors['username'] = "Please fill out the form"
        else:
            user = User.objects.filter(username = postData['username'])
            print(user)
            if user:
                current = user[0]
                if bcrypt.checkpw(postData['password'].encode(), current.password.encode()):
                    print("password match")
                    if len(postData['password']) < 8:
                        errors["password"] = "Password at least be 8 characters"
                else:
                    print("failed password")
                    errors['password'] = "Incorrect password"
            else:
                errors["username"] = "Sorry :( Not a registered username"
        return errors

class User (models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

    def __repr__(self):
        return f"<User object: {self.name} ({self.id})>"


class Travel_Manager(models.Manager):
    def travel_validator(self, postData):
        errors={}
        if len(postData['destination']) == 0 and len(postData['description']) == 0 and len(postData['start_date']) == 0 and len(postData['end_date']) == 0:
             errors['destination'] = "Please fill out the form"
        else: 
            if len(postData['destination']) < 1 :
                errors['destination'] = "Destination field cannot be empty"
            if len(postData['description']) < 1 :
                errors['description'] = "Description field cannot be empty"
            if str(datetime.now()) > postData['start_date']:
                errors['start_date'] = "Please input a valid date. Note: Start time can not be in the past"
            if str(datetime.now()) > postData['end_date']:
                errors['end_date'] = "Please input a valid date. Note: End date must be in the future"
            if postData['start_date'] > postData['end_date']:
                errors['start_date'] = "Travel Date From can not be in the future of Travel Date To"
        return errors



class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(User, related_name= "created_trip", on_delete = models.CASCADE)
    trip_member = models.ManyToManyField(User, related_name= "joined_trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Travel_Manager()
