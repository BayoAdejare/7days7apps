from django.db import models
from django.contrib.auth.models import User

import Image
from django.conf import settings
import os.path
import re
import shutil

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    best_answers = models.IntegerField(default = 0)
    answers = models.IntegerField(default = 0)
    points = models.IntegerField(default = 100)
    
    def save(self):
        super(UserProfile, self).save()
    
    class Admin:
        pass

class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(unique = True)
    
    def save(self):
        self.slug = slugify(self.name)
        super(Category, self).save()
    
    def get_absolute_url(self):
        return '/cat/%s/' % self.slug
    
    def get_ask_url(self):
        return '/ask/%s/' % self.slug    
    
    def __str__(self):
        return self.name
        
    class Admin:
        pass    

class Question(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length = 300)
    description = models.TextField()
    is_open = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add = 1)
    best_answer = models.ForeignKey('Answer', related_name = 'best_answer_for', null = True)
    latest_answered = models.DateTimeField(auto_now_add = True)#Updated whenever we have a new answer
    
    def get_absolute_url(self):
        return '/answer/%s/' % self.id
    
    def closing_url(self):
        return '/close/%s/' % self.id  

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_on',)
    
    class Admin:
        pass    
    
class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    created_on = models.DateTimeField(auto_now_add = 1)
    text = models.TextField()
    is_best = models.BooleanField(default = False)
    points = models.BooleanField(default = 1)
    
    class Meta:
        ordering = ('-is_best', )
    
    def bestify_url(self):
        return '/bestify/%s/' % self.id  
    
    def __str__(self):
        return self.text    
    
    class Admin:
        pass    
    
def slugify(string):
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()

