from django import newforms as forms
from django.core.exceptions import ObjectDoesNotExist
import re

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
        self.fields['job'].choices = [('', '--')] + [(job.name, job.name) for job in jobs]
        
    def save(self):
        job = Job.objects.get(name = self.cleaned_data['job'])
        tag, created = Tag.objects.get_or_create(name=self.cleaned_data['tag'], user = self.user)
        entry = Entry(job = job, name = self.cleaned_data['name'], tag = tag, date=self.cleaned_data['date'], \
                    hours_worked = self.cleaned_data['hours_worked'], minutes_worked = self.cleaned_data['minutes_worked'], \
                    description = self.cleaned_data['description'])
        entry.save()
        return entry
    
    job = forms.ChoiceField()
    name = forms.CharField(max_length = 100)
    tag = forms.CharField(max_length = 100)
    date = forms.DateField()
    hours_worked = forms.IntegerField()
    minutes_worked = forms.IntegerField()
    description = forms.CharField(required = False, widget=forms.Textarea)
    
    
class UserCreationForm(forms.Form):
    """A form that creates a user, with no privileges, from the given username and password."""
    username = forms.CharField(max_length = 30, required = True)
    password1 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    password2 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)

    def clean_username (self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['username']):
            raise ValidationError("This value must contain only letters, numbers and underscores.")
        self.isValidUsername()
        return self.cleaned_data['username']

    def clean (self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_("The two password fields didn't match."))
        return super(forms.Form, self).clean()
        
    def isValidUsername(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return
        raise ValidationError(_('A user with that username already exists.'))
    
    def save(self):
        User.objects.create_user(self.cleaned_data['username'], '', self.cleaned_data['password1'])    
    
class FormCollection:
    def __init__(self, FormClass, attrs, num_form):
        self.data = []
        for i in xrange(num_form):
            self.data.append(FormClass(prefix = i, **attrs))
        