from django import newforms as forms
from models import *
import re

from django.contrib.auth.models import User
from django.newforms import ValidationError
from django.utils.translation import ugettext as _

class UserCreationForm(forms.Form):
    """A form that creates a user, and adds a projectset for her"""
    username = forms.CharField(max_length = 30, required = True)
    password1 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    password2 = forms.CharField(max_length = 30, required = True, widget = forms.PasswordInput)
    projset_name = forms.CharField(max_length = 30)

    def clean_username (self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['username']):
            raise ValidationError("This value must contain only letters, numbers and underscores.")
        self.isValidUsername()
        return self.cleaned_data['username']
    
    def clean_projset_name(self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['projset_name']):
            raise ValidationError("This value must contain only letters, numbers and underscores.")
        self.isValidProjsetname()
        return self.cleaned_data['projset_name']

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
    
    def isValidProjsetname(self):
        try:
            Projset.objects.get(name=self.cleaned_data['projset_name'])
        except Projset.DoesNotExist:
            return
        raise ValidationError(_('A project set with that username already exists.'))    
    
    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'], '', self.cleaned_data['password1'])
        projset = Projset(name = self.cleaned_data['projset_name'], user = user)
        projset.save()
        return user
    
class AddProjectForm(forms.Form):
    name = forms.CharField(max_length = 100)
    
    def __init__(self, projset, user, *args, **kwargs):
        self.projset = projset
        self.user = user
        super(AddProjectForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        alnum_re = re.compile(r'^\w+$')
        if not alnum_re.search(self.cleaned_data['name']):
            raise ValidationError("This value must contain only letters, numbers and underscores.")
        try:
            Project.objects.get(name = self.cleaned_data['name'], projset = self.projset)
        except Project.DoesNotExist:
            return self.cleaned_data['name']
        raise ValidationError(_('A project with that name already exists.'))
    
    def save(self):
        project = Project(projset = self.projset, name = self.cleaned_data['name'])
        project.save()
        project.users.add(self.user)
        return project
    
class AddTodoItemForm(forms.Form):
    name = forms.CharField(max_length = 100)
    user = forms.ChoiceField()
    
    def __init__(self, project, *args, **kwargs):
        self.project = project
        super(AddTodoItemForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = [('None', 'None'), ] + [(user.username, user.username) for user in project.users.all()]
        
    def save(self):
        item = TodoItem(item = self.cleaned_data['name'])
        if not self.cleaned_data['user'] == 'None':
            user = User.objects.get(username = self.cleaned_data['user'])
            item.user = user
        item.project = self.project
        item.save()
        return item
    
class AddMilestoneForm(forms.Form):
    name = forms.CharField(max_length = 100)
    description = forms.CharField(widget = forms.Textarea)
    due_on = forms.DateTimeField()
    
    def __init__(self, project, *args, **kwargs):
        self.project = project
        super(AddMilestoneForm, self).__init__(*args, **kwargs)
        
    def save(self):
        milestone = Milestone(name = self.cleaned_data['name'], description=self.cleaned_data['description'], due_on = self.cleaned_data['due_on'])
        milestone.project = self.project
        milestone.save()
        return milestone
    
class DoChatForm(forms.Form):
    text = forms.CharField(widget = forms.Textarea)
    
    def __init__(self, project = None, user = None, *args, **kwargs):
        self.project = project
        self.user = user
        super(DoChatForm, self).__init__(*args, **kwargs)
        
    def save(self):
        chat = ChatItem(text = self.cleaned_data['text'])
        chat.user = self.user
        chat.project = self.project
        chat.save()
        return chat
    
class InviteUserForm(forms.Form):
    name = forms.CharField(max_length = 100)
    
    def clean_user(self):
        try:
            User.objects.get(username = self.cleaned_data['name'])
        except User.DoesNotExist, e:
            raise ValidationError("No user with that username")
        return self.cleaned_data['name']
    
    def __init__(self, project=None, *args, **kwargs):
        self.project = project
        super(InviteUserForm, self).__init__(*args, **kwargs)
    
    def save(self):
        user = User.objects.get(username = self.cleaned_data['name'])
        self.project.invited_users.add(user)
    