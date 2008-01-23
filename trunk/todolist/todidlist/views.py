from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import tforms
import models
import defaults
import urllib
from decorators import handle404

def index(request):
    user_todo_lists = models.TodoList.objects.filter(user = request.user)
    user = request.user
    if request.user.is_authenticated():
        public_todo_lists = models.TodoList.objects.filter(is_public = True).exclude(user = request.user)[:5]
    else:
        public_todo_lists = models.TodoList.objects.filter(is_public = True)[:5]
    payload = {'user_todo_lists':user_todo_lists,'public_todo_lists':public_todo_lists}
    return render(request, 'todidlist/main.html', payload)


@login_required
def create(request):
    if request.method == 'POST':
        form = tforms.NewListFactory.get_new_list(request, defaults.num_choices_default, request.POST)
        if form.is_valid():
            todo_list = form.save()
            return HttpResponseRedirect(todo_list.get_absolute_url())
    elif request.method == 'GET':
        try:
            num_choices = int(request.GET['choices'])
        except KeyError, e:
            num_choices = defaults.num_choices_default
        if num_choices > defaults.num_choices_max:
            raise Exception()
        form = tforms.NewListFactory.get_new_list(request, num_choices)
    more_choices = min(num_choices + 4, defaults.num_choices_max);
    more_choices_url = '/create/?'+urllib.urlencode({'choices':more_choices})
    payload = {'form':form, 'more_choices_url':more_choices_url}
    return render(request, "todidlist/create.html", payload)

@handle404
def list_detail(request, list_id):
    todo_list = models.TodoList.objects.get(id = list_id)
    if not todo_list.is_public:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/not/')
        if not request.user == todo_list.user:
            return HttpResponseRedirect('/not/')
    todo_items = models.TodoItems.objects.filter(todo_list = todo_list)
    completed_items = models.TodoItems.objects.filter(todo_list = todo_list, completed = True).count()
    uncomplete_items = models.TodoItems.objects.filter(todo_list = todo_list, completed = False).count()    
    payload = {'todo_list':todo_list,'todo_items':todo_items, 'completed_items':completed_items, 'uncomplete_items':uncomplete_items}
    return render(request, 'todidlist/details.html', payload)

@login_required
@handle404
def edit_detail(request, list_id):
    todo_list = models.TodoList.objects.get(id = list_id)
    if not todo_list.user == request.user:
        return HttpResponseRedirect('/not/')
    if request.method == 'POST':
        form = tforms.EditListForm(request.POST, instance = todo_list)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(todo_list.get_absolute_url())
    if request.method == 'GET':
        form = tforms.EditListForm(instance = todo_list)
    payload = {'form':form}
    return render(request, 'todidlist/edit.html', payload)    

@login_required
@handle404
def edit_item(request, item_id):
    todo_item = models.TodoItems.objects.get(id = item_id)
    if not todo_item.todo_list.user == request.user:
        return HttpResponseRedirect('/not/')    
    if request.method == 'POST':
        form = tforms.EditItemForm(request.POST, instance = todo_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(todo_item.todo_list.get_absolute_url())
    if request.method == 'GET':
        form = tforms.EditItemForm(instance = todo_item)
    payload = {'form':form}
    return render(request, 'todidlist/edit.html', payload)

@handle404
def view_item(request, item_id):
    todo_item = models.TodoItems.objects.get(id = item_id)
    payload = {'todo_item':todo_item}
    return render(request, 'todidlist/item.html', payload)

@login_required
def manage(request):
    todo_lists_complete = models.TodoList.objects.filter(user = request.user, completed = True)
    todo_lists_incomplete = models.TodoList.objects.filter(user = request.user, completed = False)
    payload = {'todo_list_complete':todo_lists_complete, 'todo_list_incomplete':todo_lists_incomplete}
    return render(request, "todidlist/manage.html", payload)

def create_user(request):
    if request.method == 'POST':
        form = tforms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            from django.contrib.auth import authenticate, login
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            #login(request, user)
            return HttpResponseRedirect('/')
    if request.method == 'GET':
        form = tforms.UserCreationForm()
    payload = {'form':form}
    return render(request, 'registration/create_user.html', payload)

def render(request, template, payload):
    if request.user.is_authenticated():
        todo_lists_ = models.TodoList.objects.filter(user = request.user)
    else: todo_lists_ = {}
    print todo_lists_
    payload.update({'todo_lists_':todo_lists_})
    return render_to_response(template, payload, RequestContext(request))
    
    