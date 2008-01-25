from django.http import HttpResponse, HttpResponseRedirect
#from django.views.generic.simple import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext

import tforms
from models import *
import defaults

def index(request):
    return direct_to_template(request, 'mytym/index.html', {})

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
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user,), num_form = num_rows).data        
    entries = Entry.objects.all()
    form = forms[0]
    payload = {'forms':forms, 'entries':entries, 'form':form}
    return render(request, 'mytym/entries.html', payload)

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

def entry_details(request, id):
    entry = Entry.objects.get(id = id)
    payload = {'entry':entry}
    return render(request, 'mytym/entrydetails.html', payload)

def category(request, id):
    tag = Tag.objects.get(id = id)
    entries = Entry.objects.filter(tag = tag)
    jobs = Job.objects.filter(default_tag = tag)
    payload = {'tag':tag, 'events':entries, 'jobs':jobs}
    return render(request, 'mytym/category.html', payload)
    
def render(request, template, payload):
    payload.update(get_sidebar_data())
    return render_to_response(template, payload, RequestContext(request))

def get_sidebar_data():
    recent_jobs = Job.objects.all()[:5]
    recent_categories = Tag.objects.all()[:5]
    return {'recent_jobs':recent_jobs,'recent_categories':recent_categories}