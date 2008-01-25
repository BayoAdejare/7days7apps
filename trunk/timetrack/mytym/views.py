from django.http import HttpResponse, HttpResponseRedirect
#from django.views.generic.simple import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import tforms
from models import *
import defaults

def index(request):
    return render(request, 'mytym/index.html', {})

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
    jobs = Job.objects.all()
    payload = {'form':form, 'jobs':jobs, 'forms':forms}
    return render(request, 'mytym/jobs.html', payload)

@login_required
def job_details(request, id):
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
        job = Job.objects.get(id = id)
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
        num_rows = defaults.num_rows
        request.session['num_rows'] = num_rows
        try:
            num_rows = request.GET['rows']
        except:
            pass
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user,), num_form = num_rows).data        
    entries = Entry.objects.all()
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
def entry_details(request, id):
    entry = Entry.objects.get(id = id)
    payload = {'entry':entry}
    return render(request, 'mytym/entrydetails.html', payload)

@login_required
def category(request, id):
    tag = Tag.objects.get(id = id)
    entries = Entry.objects.filter(tag = tag)
    jobs = Job.objects.filter(default_tag = tag)
    payload = {'tag':tag, 'events':entries, 'jobs':jobs}
    return render(request, 'mytym/category.html', payload)
    
@login_required
def stats(request):
    total_jobs = Job.objects.filter(user = request.user).count()
    total_events = Entry.objects.filter(job__user = request.user).count()
    time_worked = total_worked(request.user)
    job_hours, tag_hours = job_worked(request.user)
    job_hr = [(job[0], int(job[1])) for job in job_hours]
    tag_hr = [(tag[0], int(tag[1])) for tag in tag_hours]
    payload = {'total_jobs':total_jobs, 'total_events':total_events, 'time_worked':time_worked, 'job_hr':job_hr, 'tag_hr':tag_hr}
    return render(request, 'mytym/stats.html', payload)
    
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