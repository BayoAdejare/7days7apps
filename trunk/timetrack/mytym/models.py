from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    """A job or an entry can be tagged with this."""
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.name
    
    class Admin:
        pass

class Job(models.Model):
    """A job for which we are tracking time. User is the user who created this job. Default tag tags all entries under this job."""
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    default_tag = models.ForeignKey(Tag)
    
    def __str__(self):
        return self.name
    
    class Admin:
        pass
    
class Entry(models.Model):
    """Detailed data about a job. Each time you want to work on a job, you would like to add an entry here."""
    job = models.ForeignKey(Job)
    name = models.CharField(max_length = 100)
    tag = models.ForeignKey(Tag)
    date = models.DateField(auto_now_add = 1)
    hours_worked = models.PositiveIntegerField()
    minutes_worked = models.PositiveIntegerField(null = True)
    description = models.TextField(null = True)
    
    def __str__(self):
        return self.name
    
    class Admin:
        pass
    
    
    
    
