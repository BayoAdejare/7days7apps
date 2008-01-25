from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
#from django.views.generic.simple import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

import tforms
from models import *
import defaults

def handle404 (view_function):
    """If we are not in debug mode, convert ObjectDoesNotExist to Http404"""
    def wrapper (*args, **kwargs):
        if not settings.DEBUG:
            try:
                return view_function (*args, **kwargs)
            except ObjectDoesNotExist:
                raise Http404
        else:
            return view_function (*args, **kwargs)
    return wrapper

def index(request):
    if request.user.is_anonymous():
        return render(request, 'mytym/index.html', {})
    else:
        return stats(request)

@login_required
def handle_jobs(request):
    """Creates jobs and displays the Jobs page"""
    if request.method == 'POST':
        num_rows = request.session['num_rows']
        del request.session['num_rows']        
        forms = tforms.FormCollection(tforms.JobsForm, {'data':request.POST}, num_form = num_rows).data
        for form in forms:
            if form.is_valid():
                form.set_user(request.user)
                job = form.save()        
        return HttpResponseRedirect('.')
    if request.method == 'GET':       
        num_rows = defaults.num_rows
        request.session['num_rows'] = num_rows        
        forms = tforms.FormCollection(tforms.JobsForm, {}, num_form = num_rows).data
        form = forms[0]
    jobs = Job.objects.filter(user = request.user)
    payload = {'form':form, 'jobs':jobs, 'forms':forms}
    return render(request, 'mytym/jobs.html', payload)

@login_required
@handle404
def job_details(request, id):
    job = Job.objects.get(id = id)
    if not job.user == request.user:
        return HttpResponseForbidden('Unauthorised access')
    if request.method == 'POST':
        num_rows = request.session['num_rows']
        del request.session['num_rows']
        forms = tforms.FormCollection(tforms.EntryFormQuick, {'user':request.user, 'data':request.POST}, num_form = num_rows).data
        for form in forms:
            if form.is_valid():
                job = form.save()
        return HttpResponseRedirect('.')
    if request.method == 'GET':
        num_rows = defaults.num_rows
        request.session['num_rows'] = num_rows    
        entries = Entry.objects.filter(job = job)
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user, initial = {'job':job.name}), num_form = num_rows).data
        form = forms[0]
        payload = {'job':job, 'entries':entries, 'forms':forms, 'form':form}
        return render(request, 'mytym/job.html', payload)

@login_required
def handle_entries(request):
    """Creates entries from jobs and displays the entries page"""
    if request.method == 'POST':
        num_rows = request.session['num_rows']
        del request.session['num_rows']
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user, data=request.POST), num_form = num_rows).data
        for form in forms:    
            if form.is_valid():
                entry = form.save()
        return HttpResponseRedirect('.')
    if request.method == 'GET':
        entries = Entry.objects.filter(job__user = request.user)
        num_rows = defaults.num_rows
        request.session['num_rows'] = num_rows
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user,), num_form = num_rows).data        
    form = forms[0]
    payload = {'forms':forms, 'entries':entries, 'form':form}
    return render(request, 'mytym/entries.html', payload)

@login_required
def detailed_entry(request):
    """Creates entries for jobs."""
    if request.method == 'POST':
        print request.POST
        form = tforms.EntryForm(request.user, request.POST)
        if form.is_valid():
            entry = form.save()
            try:
                request.POST['Save']
                return HttpResponseRedirect('.')
            except KeyError, e:
                return HttpResponseRedirect(entry.job.get_absolute_url())            
    if request.method == 'GET':
        form = tforms.EntryForm(request.user)
    payload = {'form':form}
    return render(request, 'mytym/entry.html', payload)

@login_required
@handle404
def entry_details(request, id):
    entry = Entry.objects.get(id = id)
    if not entry.job.user == request.user:
        return HttpResponseForbidden('Unauthorised access')    
    payload = {'entry':entry}
    return render(request, 'mytym/entrydetails.html', payload)

@login_required
@handle404
def category(request, id):
    tag = Tag.objects.get(id = id)
    if not tag.user == request.user:
        return HttpResponseForbidden('Unauthorised access')    
    entries = Entry.objects.filter(tag = tag)
    jobs = Job.objects.filter(default_tag = tag)
    payload = {'tag':tag, 'events':entries, 'jobs':jobs}
    return render(request, 'mytym/category.html', payload)
    
@login_required
def stats(request):
    total_jobs = Job.objects.filter(user = request.user).count()
    total_events = Entry.objects.filter(job__user = request.user).count()
    job_hours, tag_hours = job_worked(request.user)
    try:
        time_worked = total_worked(request.user)
        job_hr = [(job[0], int(job[1])) for job in job_hours]
        tag_hr = [(tag[0], int(tag[1])) for tag in tag_hours]
    except:
        time_worked = 0
        job_hr = []
        tag_hr = []        
    payload = {'total_jobs':total_jobs, 'total_events':total_events, 'time_worked':time_worked, 'job_hr':job_hr, 'tag_hr':tag_hr}
    return render(request, 'mytym/stats.html', payload)

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
    payload.update(get_sidebar_data(request))
    return render_to_response(template, payload, RequestContext(request))

def get_sidebar_data(request):
    if not request.user.is_anonymous():
        recent_jobs = Job.objects.filter(user = request.user)[:5]
        recent_categories = Tag.objects.filter(user = request.user)[:5]
        return {'recent_jobs':recent_jobs,'recent_categories':recent_categories}
    else:
        return {}