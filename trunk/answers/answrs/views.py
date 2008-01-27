from django.http import HttpResponse, HttpResponseRedirect
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext

import aforms

def index(request):
    userp = request.user.get_profile()
    return HttpResponse(userp.get_pic_url())

def ask(request):
    """Ask a question"""
    if request.method == 'POST':
        form = aforms.QuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(question.get_absolute_url())
    elif request.method == 'GET':
        form = aforms.QuestionForm()
    payload = {'form':form}
    return render(request, 'answrs/ask.html', payload)

def add_cat(request):
    """Add a category"""
    if request.method == 'POST':
        form = aforms.CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            return HttpResponseRedirect(cat.get_absolute_url())
    elif request.method == 'GET':
        form = aforms.CategoryForm()
        payload = {'form':form}
        return render(request, 'answrs/add_cat.html', payload)
    
def answer(request, id):
    """Answer the question with the given id"""
    question = Question.objects.get(id = id)
    answers = question.answer_set.all()
    if request.method == 'POST':
        form = aforms.AnswerForm(user = request.user, question = question, data = request.POST)
        print 'asdf'
        if form.is_valid():
            answer = form.save()
            return HttpResponseRedirect('.')   
    elif request.method == 'GET':
        form = aforms.AnswerForm()
    payload = {'question':question, 'answers':answers, 'form':form, }
    return render(request, 'answrs/answers.html', payload)
    
def view_cat(request, slug):
    """Shows a actegory page"""
    cat = Category.objects.get(slug = slug)
    return HttpResponse(cat.name)

def profile(request, username = None):
    """Shows a profile page"""
    if username == None:
        user = request.user
    else:
        user = User.objects.get(username = username)
    profile = user.get_profile()
    if request.method == 'POST':
        form = aforms.ProfileImageForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
    elif request.method == 'GET':
        form = aforms.ProfileImageForm(instance = profile)
    payload = {'form':form, 'profile':profile, 'user':user }
    return render(request, 'answrs/profile.html', payload)
    
    
def render(request, template, payload):
    return render_to_response(template, payload, RequestContext(request))
    
