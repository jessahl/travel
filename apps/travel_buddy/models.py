# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['name']) < 2 or len(postData['username']) < 2:
            errors['name_error'] = 'Name and/or username must be 2 or more characters'
            
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not a valid email'
        
        if postData['birthday'] == '':
            errors['birthday'] = 'Please enter your birthday'
        
        if len(postData['password']) < 8 or len(postData['confirm_password']) <8:
            errors['pass_length'] = 'Password must be 8 or more characters'   

        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = 'Passwords do not match.'          

        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already in use."   
        return errors

    def login(self, postData):
        error ={}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) >0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = {"error":"Email/Password Invalid"}
                return errors
        else:
            errors = {"error":"Login Invalid"}
            return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    birthday = models.DateField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class DestinationManager(models.Manager):
    def destination(self, postData):
        errors = {}
        print postData        
        if len(postData['destination']) or len(postData['description'])  == 0:
            errors['item_error'] = "no empty entries"
        # if postData['created_at'] > postData['date_from'] or postData['date_to']:
        #     errors['date'] = "The date cannot be in the past!"
        # if postData['date_to'] > postData['date_from']:
        #     errors['date2'] = "'Travel To Date To' should not be before the 'Travel From Date From'"
        # if errors:
            print("Error adding everything")
            return errors
        else:
            print("Added everything successfully")
            user = User.objects.get(id = int(postData['created_by']))
            new_destination = Destination.objects.create(destination = postData['item'], description = postData['description'], date_from = postData['date_from'], date_to = postData['date_to'], created_by = user )
            return {'new_destination': new_destination}

class Destination(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    joined = models.ManyToManyField(User, related_name="joined")
    created_by = models.ForeignKey(User, related_name="created_by")
    objects = DestinationManager()