from django.db import models
from django.contrib.auth.models import User
from django.db import connection

class Tag(models.Model):
    """A job or an entry can be tagged with this."""
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User)
    create_on = models.DateTimeField(auto_now_add = 1)
    
    def get_absolute_url(self):
        return '/category/%s/' %self.id    
    
    def __str__(self):
        return self.name
    
    class Admin:
        pass

class Job(models.Model):
    """A job for which we are tracking time. User is the user who created this job. Default tag tags all entries under this job."""
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    default_tag = models.ForeignKey(Tag)
    created_on = models.DateTimeField(auto_now_add = 1)
    
    def total_hrs_worked(self):
        """Total hours worked for this job. Summ all hours worked for entriesunder this job"""
        cursor = connection.cursor()
        cursor.execute("SELECT sum(hours_worked)+sum(minutes_worked)/60 FROM mytym_entry WHERE job_id = %s", [self.id])
        row = cursor.fetchone()
        return int(row[0])
    
    def num_events(self):
        """Number of ebents for this job."""
        return Entry.objects.filter(job = self).count()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/jobdetails/%s/' %self.id
    
    class Admin:
        pass
    
    class Meta:
        ordering = ('-created_on', )
    
class Entry(models.Model):
    """Detailed data about a job. Each time you want to work on a job, you would like to add an entry here."""
    job = models.ForeignKey(Job)
    name = models.CharField(max_length = 100)
    tag = models.ForeignKey(Tag)
    date = models.DateField(auto_now_add = 1)
    created_on = models.DateTimeField(auto_now_add = 1)
    hours_worked = models.PositiveIntegerField()
    minutes_worked = models.PositiveIntegerField(default = 0)
    description = models.TextField(null = True)
    
    def time_worked(self):
        return self.hours_worked + self.minutes_worked/60
    
    def get_absolute_url(self):
        return '/entrydetails/%s/' % self.id    
    
    def __str__(self):
        return self.name
    
    class Admin:
        pass
    
    class Meta:
        ordering = ('-created_on', )
        

#helpers
def total_worked(user):
    cursor = connection.cursor()
    cursor.execute("SELECT sum(hours_worked) FROM mytym_entry, mytym_job, auth_user WHERE mytym_entry.job_id = mytym_job.id AND auth_user.id = mytym_job.user_id AND auth_user.id = %s", [user.id])
    row = cursor.fetchone()
    return int(row[0])

def job_worked(user):
    cursor = connection.cursor()
    cursor.execute("SELECT mytym_job.name, sum(hours_worked) FROM mytym_entry, mytym_job, auth_user WHERE mytym_entry.job_id = mytym_job.id AND auth_user.id = mytym_job.user_id AND auth_user.id = %s GROUP BY mytym_job.name ", [user.id])
    job_hours = cursor.fetchall()
    cursor.execute("SELECT mytym_tag.name, sum(hours_worked) FROM mytym_entry, mytym_tag, auth_user WHERE mytym_entry.tag_id = mytym_tag.id AND auth_user.id = mytym_tag.user_id AND auth_user.id = %s GROUP BY mytym_tag.name ", [user.id])
    tag_hours = cursor.fetchall()
    return job_hours, tag_hours
    
    
    
    
    
    
    
    
