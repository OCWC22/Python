from __future__ import unicode_literals
from django.db import models
import re

class User_Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        name_regex = re.compile(r'[a-zA-Z]')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")

        if len(postData["first_name"]) <= 0 and not name_regex.match(postData["first_name"]):
            errors["first_name"] = "First name cannot be blank and mus tonly have letters"

        if len(postData["last_name"]) <= 0 and not name_regex.match(postData["last_name"]):
            errors["last_name"] = "Last name cannot be blank and must only have letters"
        if len(postData["password"]) < 8:
            errors["password"] =  "password must be at least 8 characters"

        if postData["confirmpassword"] != postData["password"]:
            errors["confirmpassword"] = "Password does not match, try again"
        return errors

    def trip_validator(self, postData):
        errors = {}
        if len(postData["destination"]) < 3:
            errors["destination"] = "destination must be longer than 3 characters"
        if postData["start_date"] > postData["end_date"]:
            errors["start_date"] = "start date cannot be after end date"

        return errors




    """
models come with a hidden property:
      objects = models.Manager()
we are going to override this!
"""
class User (models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()
    #def __repr__(self):
        #return str(self.__dict__)

class Trip (models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.ForeignKey(User, related_name='trips_created', null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = User_Manager()
   

    def __repr__(self):
        return f"Trip: {self.destination}"
        #return str(self.__dict__)

