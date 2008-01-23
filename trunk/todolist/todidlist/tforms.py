import django.newforms as forms
from dynaforms import DynaForm
import models
import re
from django.contrib.auth.models import User
from django.newforms import ValidationError
from django.utils.translation import ugettext as _

class NewListFactory:
    @classmethod
    def get_new_list(self, request, num_choices = 8, *args, **kwargs):
        class NewList(DynaForm):
            list_name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'size':60, 'class':'main'}), help_text = 'Name of your list. This field is required.')
            choices = [forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'size':60}), required = False)] * num_choices
            is_public = forms.BooleanField(initial = True, help_text = 'Should we make this list public?')
            complete = forms.BooleanField(initial = False)
            def set_initial(self, todo_list = None, todo_items=None):
                print self.fields
                if not todo_list == None:
                    self.fields['list_name'].initial = todo_list.list_name
                if not todo_items == None:
                    self.fields['choices_1'].initial = '1000'
                    self.fields['choices_2'].initial = '21'
                    for i in xrange(len(todo_items)):
                        field_name = 'choices %s' % (i+1)
            def set_request(self, request):
                self.request = request
            def save(self):
                todo_list = models.TodoList(user = self.request.user, list_name = self.cleaned_data['list_name'])
                todo_list.save()
                for k, v in self.cleaned_data.items():
                    if k in ('list_name', 'is_public'):
                        continue
                    else:
                        if v:
                            choice = models.TodoItems(todo_list = todo_list, item = v)
                            choice.save()
                return todo_list
        list_form = NewList(*args, **kwargs)
        list_form.set_request(request)
        return list_form
    
class EditListForm(forms.ModelForm):
    list_name = forms.CharField(widget = forms.TextInput(attrs = {'size':60}))
    is_public = forms.BooleanField(help_text = 'Should list be publically available?')
    completed = forms.BooleanField(help_text = 'Are todo items for this list done?')
    class Meta:
        model = models.TodoList
        exclude = ('user', )
    def save(self):
        todo_items = models.TodoItems.objects.filter(todo_list__list_name__exact = self.cleaned_data['list_name'])
        for item in todo_items:
            item.completed = True
            item.save()
            super(EditListForm, self).save()
        
    
class EditItemForm(forms.ModelForm):
    description = forms.CharField(required = False, widget = forms.Textarea)
    complete_by = forms.DateField(required = False, help_text = 'Eg. 2006-10-25')# input_formats = '%m/%d/%Y')
    class Meta:
        model = models.TodoItems
        exclude = ('todo_list', 'ordering')
        
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

    
    
