from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
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
        form = tforms.JobsForm(request.POST)
        if form.is_valid():
            form.set_user(request.user)
            job = form.save()
            return HttpResponseRedirect('.')
    if request.method == 'GET':
        form = tforms.JobsForm()
    jobs = Job.objects.all()
    payload = {'form':form, 'jobs':jobs}
    return render(request, 'mytym/jobs.html', payload)

"""
def handle_entries(request):
    "Creates entries fro jobs and displays the entries page"
    if request.method == 'POST':        
        form = tforms.EntryFormQuick(user = request.user, data=request.POST, prefix='xd')
        print request.POST
        print form.fields
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('.')
    if request.method == 'GET':
        form = tforms.EntryFormQuick(user=request.user, prefix='xd')
        #form2 = tforms.EntryFormQuick(request.user, prefix='xd')
    entries = Entry.objects.all()
    payload = {'form':form, 'entries':entries}
    return render(request, 'mytym/entries.html', payload)
"""
def handle_entries(request):
    """Creates entries fro jobs and displays the entries page"""
    if request.method == 'POST':        
        form = tforms.EntryFormQuick(user = request.user, data=request.POST, prefix='xd')
        print request.POST
        print form.fields
        if form.is_valid():
            entry = form.save()
            return HttpResponseRedirect('.')
    if request.method == 'GET':
        forms = tforms.FormCollection(tforms.EntryFormQuick, dict(user=request.user), num_form = 10)
        #form2 = tforms.EntryFormQuick(request.user, prefix='xd')
    entries = Entry.objects.all()
    form = forms.data[0]
    print form
    payload = {'forms':forms, 'entries':entries, 'form':form}
    return render(request, 'mytym/entries.html', payload)

    
def get_multi_form():
    pass
    
def render(request, template, payload):
    return render_to_response(template, payload, RequestContext(request))
