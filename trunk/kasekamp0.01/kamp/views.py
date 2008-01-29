from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import *
import kforms
from decorators import *

def index(request):
    if request.user.is_authenticated():
        projset = Projset.objects.get(user = request.user)
        return HttpResponseRedirect(projset.get_absolute_url())
    else:
        return HttpResponseRedirect('/accounts/login/')


@login_required
def dashboard(request, projset):
    projset = Projset.objects.get(name = projset)
    if not projset.user == request.user:
        raise Http404
    projects = projset.project_set.all()
    if request.method == 'GET':
        form = kforms.AddProjectForm(projset, request.user)
    if request.method == 'POST':
        form = kforms.AddProjectForm(projset, request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
    payload = locals()
    return render(request, 'kamp/dashboard.html', payload)
    
@login_required
def project_summary(request, projset, id):
    projset = Projset.objects.get(name = projset)
    project = projset.project_set.get(id = id)
    check_user_has_access(project, request.user)
    todo_items = project.todoitem_set.filter(completed = False)[:5]
    milestones = project.milestone_set.filter(completed = False)[:5]
    if request.method == 'POST':
        form = kforms.InviteUserForm(project, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
    if request.method == 'GET':
        form  = kforms.InviteUserForm(project)
    payload = locals()
    return render_proj(request, 'kamp/project_summary.html', payload, project)

@login_required
def milestones(request, projset, id):
    projset = Projset.objects.get(name = projset)
    project = projset.project_set.get(id = id)
    check_user_has_access(project, request.user)
    milestones = project.milestone_set.filter(completed = False)
    milestones_reached = project.milestone_set.filter(completed = True)
    if request.method == 'GET':
        form = kforms.AddMilestoneForm(project)
    if request.method == 'POST':
        if request.POST.has_key('markdone') or request.POST.has_key('markundone'):
            try:
                id = request.POST['markdone']
            except KeyError, e:
                id = request.POST['markundone']
            milestone = Milestone.objects.get(id = id)
            milestone.completed = not milestone.completed
            act_txt = "%s changed status for %s milestone." % (request.user, milestone.name)
            activity = ActivityStream(project = project, text = act_txt)
            activity.save()             
            milestone.save()
            return HttpResponseRedirect('.')
        else:
            form = kforms.AddMilestoneForm(project, request.POST)
            if form.is_valid():
                milestone = form.save()
                act_txt = "%s created a new milestone: %s" % (request.user, milestone.name)
                activity = ActivityStream(project = project, text = act_txt)
                activity.save()                
                return HttpResponseRedirect('.')
    payload = locals()
    return render_proj(request, 'kamp/milestones.html', payload, project)

@login_required
def todo(request, projset, id):
    projset = Projset.objects.get(name = projset)
    project = projset.project_set.get(id = id)
    check_user_has_access(project, request.user)
    todo_items = project.todoitem_set.filter(completed = False)
    todo_items_done = project.todoitem_set.filter(completed = True)
    if request.method == 'GET':
        form = kforms.AddTodoItemForm(project)
    if request.method == 'POST':
        if request.POST.has_key('markdone') or request.POST.has_key('markundone'):
            try:
                id = request.POST['markdone']
            except KeyError, e:
                id = request.POST['markundone']
            item = TodoItem.objects.get(id = id)
            item.completed = not item.completed
            act_txt = "%s changed status for %s todo." % (request.user, item.item)
            activity = ActivityStream(project = project, text = act_txt)
            activity.save()             
            item.save()
            return HttpResponseRedirect('.')
        else:
            form = kforms.AddTodoItemForm(project, request.POST)
            if form.is_valid():
                item = form.save()
                act_txt = "%s created a new todo item: %s" % (request.user, item.item)
                activity = ActivityStream(project = project, text = act_txt)
                activity.save()
                return HttpResponseRedirect('.')  
    payload = locals()
    return render_proj(request, 'kamp/todo.html', payload, project)


@login_required    
def chat(request, projset, id):
    projset = Projset.objects.get(name = projset)
    project = projset.project_set.get(id = id)
    check_user_has_access(project, request.user)
    chats = project.chatitem_set.all()
    print len(chats)
    if request.method == 'GET':
        form = kforms.DoChatForm()
    if request.method == 'POST':
        form = kforms.DoChatForm( project, request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
    payload = locals()
    return render_proj(request, 'kamp/chat.html', payload, project)

@login_required
def profile(request, user=None):
    if request.method == 'POST':
        try:
            id = request.POST['accept']
            project = Project.objects.get(id = id)
            project.users.add(request.user)
            project.invited_users.remove(request.user)
        except KeyError, e:
            id = request.POST['decline']
            project = Project.objects.get(id = id)
            project.invited_users.remove(request.user)
        return HttpResponseRedirect('.')    
    projset = Projset.objects.get(user = request.user)
    if user == None:
        user = request.user
    projects = user.project_set.all()#Project.objects.filter(users = user)
    invited_to = Project.objects.filter(invited_users = user)
    payload = locals()
    return render(request, 'registration/profile.html', payload)


def create_user(request):
    if request.method == 'POST':
        form = kforms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            from django.contrib.auth import authenticate, login
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            #login(request, user)
            return HttpResponseRedirect('/accounts/login/')
    if request.method == 'GET':
        form = kforms.UserCreationForm()
    payload = {'form':form}
    return render(request, 'registration/create_user.html', payload)


def render(request, template, payload):
    return render_to_response(template, payload, RequestContext(request))


def render_proj(request, template, payload, project):
    activities = project.activitystream_set.all()[:15]
    print len(activities)
    payload.update({'activities':activities})
    return render_to_response(template, payload, RequestContext(request))

def check_user_has_access(project, user):
    """Check that a user is in the users list for a project"""
    try:
        project.users.get(username = user.username)
    except User.DoesNotExist, e:
        raise Http404
    return