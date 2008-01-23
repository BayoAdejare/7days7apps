from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    user = models.ForeignKey(User)
    list_name = models.CharField(max_length = 100,)
    is_public = models.BooleanField(default = True)
    completed = models.BooleanField(default = False)
    def get_absolute_url(self):
        return '/list/%s/' % self.id
    
    def get_edit_url(self):
        return '/edit/%s/' % self.id      
    
    def __str__(self):
        return self.list_name
    
    class Admin:
        pass
    
class TodoItems(models.Model):
    todo_list = models.ForeignKey(TodoList)
    item = models.CharField(max_length = 100,)
    ordering = models.IntegerField(default = 1)
    description = models.TextField()
    completed = models.BooleanField(default = False)
    worth_doing = models.BooleanField(default = True)
    complete_by = models.DateField(null = True)
    def __str__(self):
        return self.item
    
    def save(self):
        num_choices = TodoItems.objects.filter(todo_list = self.todo_list).count()
        self.ordering = num_choices + 1
        super(TodoItems, self).save()
        
    def get_absolute_url(self):
        return '/viewitem/%s/' % self.id
    
    def get_edit_url(self):
        return '/edititem/%s/' % self.id    
        
    class Meta:
        get_latest_by = "ordering"
        
    class Admin:
        pass 