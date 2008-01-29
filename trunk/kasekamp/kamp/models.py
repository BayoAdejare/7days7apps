from django.db import models
from django.contrib.auth.models import User

class Projset(models.Model):
    """The project set for a user. Contains all their projects."""
    name = models.CharField(unique = True, max_length = 100)
    user = models.ForeignKey(User, unique = True)
    
    def get_absolute_url(self):
        return '/%s/' % self.name
    
    class Admin:
        pass
    
class Project(models.Model):
    """A peoject. Many users can be subscribed to a project. One user can have many projects."""
    projset = models.ForeignKey(Projset)
    active = models.BooleanField(default = True)
    name = models.CharField(max_length = 100)
    users = models.ManyToManyField(User)
    invited_users = models.ManyToManyField(User, related_name='invited_projects')#users who have been invited, but have not joined yet.
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.projset.name, self.id)
    
    #Other detail urls
    def todo_url(self):
        return '/%s/%s/todo/' % (self.projset.name, self.id)
    
    def milestones_url(self):
        return '/%s/%s/milestones/' % (self.projset.name, self.id)
    
    def chat_url(self):
        return '/%s/%s/chat/' % (self.projset.name, self.id)
    
    class Admin:
        pass
    
    class Meta:
        unique_together = ('projset', 'name')
    
class TodoItem(models.Model):
    """A item which needs to be done. It can assigned to an user, or open"""
    item = models.CharField(max_length = 100)
    user = models.ForeignKey(User, null = True)
    project = models.ForeignKey(Project)
    completed = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add = 1)
    
    class Meta:
        ordering = ('created_on',)
    
    class Admin:
        pass
    
class ChatItem(models.Model):
    """A chat item in the persistant chat of the project"""
    text = models.CharField(max_length = 200)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add = 1)
    
    class Meta:
        ordering = ('created_on',)
    
    class Admin:
        pass
    
class Milestone(models.Model):
    """A milestone for the project, this is not project specific."""
    name = models.CharField(max_length = 100)
    description = models.TextField()
    project = models.ForeignKey(Project)
    due_on = models.DateField()
    completed = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add = 1)
    
    class Meta:
        ordering = ('created_on',)
    
    class Admin:
        pass
