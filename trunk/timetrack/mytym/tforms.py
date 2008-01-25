from django import newforms as forms
from django.core.exceptions import ObjectDoesNotExist

from models import *

class JobsForm(forms.Form):
    name = forms.CharField(max_length = 100)
    default_tag = forms.CharField(max_length = 50)
    def set_user(self, user):
        self.user = user
    def save(self):
        tag, created = Tag.objects.get_or_create(name = self.cleaned_data['default_tag'], user = self.user)
        job = Job(name = self.cleaned_data['name'], user = self.user, default_tag = tag)
        job.save()        
 
class EntryFormQuick(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EntryFormQuick, self).__init__(*args, **kwargs)
        self.user = user
        jobs = Job.objects.filter(user = self.user)
        self.fields['job'].choices = [('', '--')] + [(job.name, job.name) for job in jobs]
        
    def save(self):
        job = Job.objects.get(name = self.cleaned_data['job'])
        entry = Entry(name = self.cleaned_data['name'], job = job, tag = job.default_tag, hours_worked = self.cleaned_data['hours_worked'])
        entry.save()
        return entry
    
    job = forms.ChoiceField()
    name = forms.CharField(max_length = 100)
    hours_worked = forms.IntegerField()
    
class EntryForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.user = user
        jobs = Job.objects.filter(user = self.user)
        self.fields['jobs'].choices = [('', '--')] + [(job.name, job.name) for job in jobs]
    
    jobs = forms.ChoiceField()
    name = forms.CharField(max_length = 100)
    tag = forms.CharField(max_length = 100)
    date = forms.DateField()
    hours_worked = forms.IntegerField()
    minutes_worked = forms.IntegerField()
    description = forms.CharField(required = False)
    
class FormCollection:
    def __init__(self, FormClass, attrs, num_form):
        self.data = []
        for i in xrange(num_form):
            self.data.append(FormClass(prefix = i, **attrs))
        