from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from models import *
import pforms

def index(request):
    return render('pollngo/index.html', {}, request)

def question(request, slug):
    try:
        question = Question.objects.get(slug = slug)
    except ObjectDoesNotExist, e:
        raise Http404    
    if request.method == 'POST':
        try:
            last_choice_id = request.session[question.id]
            last_choice = Choice.objects.get(id = last_choice_id)
            last_choice.total_votes -= 1
            last_choice.save()
        except KeyError, e:
            pass        
        choice_id = int(request.POST['choices'])
        choice = Choice.objects.get(id = choice_id)
        choice.total_votes += 1
        choice.save()
        request.session[question.id] = choice.id
        return HttpResponseRedirect(question.get_results_url())
    if request.method == 'GET':
        try:
            last_choice_id = request.session[question.id]
            last_choice = Choice.objects.get(id = last_choice_id)
        except KeyError, e:
            last_choice = 0
        choices = Choice.objects.filter(question = question)
        payload = {'question':question, 'choices':choices, 'last_choice':last_choice}
        
        return render('pollngo/question.html', payload, request)

def results(request, slug):
    try:
        question = Question.objects.get(slug = slug)
    except ObjectDoesNotExist, e:
        raise Http404
    total_votes = 0
    for choice in question.choice_set.all():
        total_votes += choice.total_votes
    payload = {'question':question, 'total_votes':total_votes}
    return render('pollngo/results.html', payload, request)
        
    

def create(request):
    if request.method == 'POST':    
        form = pforms.CreatePoll(request, request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(question.get_absolute_url())
    elif request.method == 'GET':
        form = pforms.CreatePoll(request)
    payload = {'form':form}
    return render('pollngo/create.html', payload, request)
    
#Helper methods.
def render(template_name, payload, request):
    recent_polls = Question.objects.all()[:8]
    payload.update({'recent_polls':recent_polls})
    return render_to_response(template_name, payload, RequestContext(request))
    


