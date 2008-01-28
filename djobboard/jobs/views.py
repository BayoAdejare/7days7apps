from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response
import django.newforms as forms

import models

def index(request):
    return add_developer(request)

def handle_form(request, Form, template_name):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            object = form.save()
            return HttpResponseRedirect(object.get_absolute_url())
    if request.method == 'GET':
        form = Form()
    payload = {'form':form}
    return render_to_response(template_name, payload)

def add_developer(request):
    return handle_form(request, DeveloperForm, 'jobs/adddev.html')

def add_job(request):
    return handle_form(request, JobForm, 'jobs/addjob.html')

def developer(request, id):
    qs = models.Developer.objects.all()
    return object_detail(request, template_name = 'jobs/developer.html', queryset = qs, object_id = id, template_object_name = 'developer')
    

def job(request, id):
    qs = models.Job.objects.all()
    return object_detail(request, template_name = 'jobs/job.html', queryset = qs, object_id = id, template_object_name = 'job')

def developers(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'        
    qs = models.Developer.objects.all().order_by(order_by)
    return object_list(request, template_name = 'jobs/developers.html', queryset = qs, template_object_name = 'developers', paginate_by=10)

def jobs(request):
    try:
        order_by = request.GET['order']
    except:
        order_by = 'created_on'
    if order_by == 'created_on': order_by = '-created_on'
    if not order_by in ('name', 'created_on'):
        order_by = '-created_on'
    qs = models.Job.objects.all().order_by(order_by)
    return object_list(request, template_name = 'jobs/jobs.html', queryset = qs, template_object_name = 'jobs', paginate_by=10)

def edit_job(request, id):
    job = models.Job.objects.get(id = id)
    if not job.is_editable:
        raise Http404
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == job.password:
                request.session['job_edit_rights'] = id
                return HttpResponseRedirect(('/editjob/%s/done/' % id))
            else:
                return HttpResponseForbidden('Wrong password. Go back and try again.')
    if request.method == 'GET':
        form = PasswordForm()
    payload = {'form':form}
    return render_to_response('jobs/editdev.html', payload)

def edit_developer(request, id):
    dev = models.Developer.objects.get(id = id)
    if not dev.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = PasswordForm(request.POST)        
        if form.is_valid():
            if form.cleaned_data['password'] == dev.password:
                request.session['dev_edit_rights'] = id
                return HttpResponseRedirect(('/editdev/%s/done/' % id))
            else:
                return HttpResponseForbidden('Wrong password. Go back and try again.')
    if request.method == 'GET':
        form = PasswordForm()
    payload = {'form':form}
    return render_to_response('jobs/editdev.html', payload)

def edit_job_done(request, id):
    job = models.Job.objects.get(id = id)
    if not job.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = JobForm(request.POST, instance = job)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(job.get_absolute_url())
    elif request.method == 'GET':
        job = models.Job.objects.get(id = id)
        form = JobForm(instance = job)
    payload = {'form': form}
    return render_to_response('jobs/editjob.html', payload)
    
def edit_developer_done(request, id):
    dev = models.Developer.objects.get(id = id)
    if not dev.is_editable:
        raise Http404    
    if request.method == 'POST':
        form = DeveloperForm(request.POST, instance = dev)
        if form.is_valid():
            dev = form.save()
            return HttpResponseRedirect(dev.get_absolute_url())
    elif request.method == 'GET':
        dev = models.Developer.objects.get(id = id)
        form = DeveloperForm(instance = dev)
    payload = {'form': form}
    return render_to_response('jobs/adddev.html', payload)
    
class DeveloperForm(forms.ModelForm):
    name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'size':50, 'class':"text"}), help_text="Your or Company's name. This field is required.")
    description = forms.CharField(widget = forms.Textarea({'class':"text"}), help_text = 'Some description about you, links to sample work, testimonials etc. This field is required.')
    email = forms.EmailField(widget = forms.TextInput(attrs={'size':50, 'class':"text"}), help_text='Your email. This field is required.')
    website = forms.URLField(required = False, widget = forms.TextInput(attrs={'size':50, 'class':"text"}), help_text='Link to your website.')
    location = forms.CharField(required = False, max_length = 100, widget = forms.TextInput(attrs={'size':50, 'class':"text"}), help_text='Where are you located?')
    #Edit info
    password = forms.CharField(max_length = 100, required = False,  widget = forms.PasswordInput(attrs={'size':50, 'class':"text"}), help_text='Enter a password, if you would like to edit this in future. This password is saved in cleartext, so do not use a valuable password.')
    
    class Meta:
        model = models.Developer
        exclude = ('is_editable')
        
    def save(self):
        developer = super(DeveloperForm, self).save()
        if developer.password:
            developer.is_editable = True
            developer.save()
        return developer
        
class JobForm(forms.ModelForm):
    name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'size':50}), label='Job Name', help_text = 'Name of the job/contract')
    description = forms.CharField(max_length = 100, widget = forms.Textarea, help_text = 'Some information about the job/contract.')
    budget = forms.IntegerField(widget = forms.TextInput(attrs={'size':50}), required=False, help_text = 'Budget/Salary for this contract/job.')
    on_site = forms.BooleanField(widget = forms.TextInput(attrs={'size':50}),required=False, help_text = 'Are peole required to be on site?')
    location = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'size':50}), required=False, help_text= 'Where is this located?')
    #Posters Info
    poster_name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'size':50}), help_text = "Your /Your company's name.", label='Your Name')
    email = forms.EmailField(widget = forms.TextInput(attrs={'size':50}),help_text = 'Your email id.')
    website = forms.URLField(widget = forms.TextInput(attrs={'size':50}), required=False, help_text = 'Your website.')
    other_info = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'size':50}), required=False, help_text = 'Some information about you.')
    #Edit info
    password = forms.CharField(max_length = 100, required = False, widget = forms.PasswordInput(attrs={'size':50}), help_text = 'If you want this job to be editable, enter a password. This password is saved in cleartext, so do not use a valuable password.')
    
    class Meta:
        model = models.Job
        exclude = ('is_editable')
        
    def save(self):
        job = super(JobForm, self).save()
        if job.password:
            job.is_editable = True
            job.save()
        job.save()
        return job
        
class PasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'size':50}), help_text = 'Enter the passwords assocoiated with this posting.')
