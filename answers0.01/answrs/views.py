from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime
import random
from decorators import handle404
import aforms

def index(request):
    return render(request, 'answrs/index.html', {})

@handle404
@login_required
def ask(request, category_slug = None):
    """Ask a question"""
    if category_slug:
        cat = Category.objects.get(slug = category_slug)
    else:
        cat = None
    if request.method == 'POST':
        form = aforms.QuestionForm(request.user, cat, request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(question.get_absolute_url())
    elif request.method == 'GET':
        form = aforms.QuestionForm(request.user, cat)
    payload = {'form':form}
    return render(request, 'answrs/ask.html', payload)

@login_required
def add_cat(request):
    """Add a category"""
    if not request.user.is_staff:
        return HttpResponseForbidden('Not Allowed')
    if request.method == 'POST':
        form = aforms.CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            return HttpResponseRedirect(cat.get_absolute_url())
    elif request.method == 'GET':
        form = aforms.CategoryForm()
        payload = {'form':form}
        return render(request, 'answrs/add_cat.html', payload)

@handle404
@login_required
def answer(request, id):
    """Answer the question with the given id"""
    question = Question.objects.get(id = id)
    answers = question.answer_set.all()
    if request.method == 'POST':
        form = aforms.AnswerForm(user = request.user, question = question, data = request.POST)
        if form.is_valid():
            answer = form.save()
            question.latest_answered = datetime.datetime(1900, 1, 1).now()
            question.save()
            profile = answer.user.get_profile()
            profile.answers += 1
            profile.points += 2
            profile.save()
            return HttpResponseRedirect('.')   
    elif request.method == 'GET':
        form = aforms.AnswerForm()
    payload = {'question':question, 'answers':answers, 'form':form, }
    return render(request, 'answrs/answers.html', payload)

@handle404
@login_required
def view_cat(request, slug):
    """Shows a actegory page"""
    cat = Category.objects.get(slug = slug)
    questions = cat.question_set.all()[:10]
    payload = {'category':cat, 'questions':questions}
    return render(request, 'answrs/view_cat.html', payload)

@handle404
@login_required
def close(request, id):
    """Yes, I know, I know, this is a huge CSRF hole, but I am so sleepy now. I will come back to it, promise."""
    question = Question.objects.get(id = id)
    question.is_open = False
    question.save()
    return HttpResponseRedirect(question.get_absolute_url())

@handle404
@login_required
def bestify(request, id):
    """Yes, I know, I know, this is a huge CSRF hole, but I am so sleepy now. I will come back to it, promise."""
    answer = Answer.objects.get(id = id)
    profile = answer.user.get_profile()
    profile.best_answers += 1
    profile.points += 5
    profile.save()
    question = answer.question
    question.best_answer = answer
    answer.is_best = True
    question.save()
    answer.save()
    return HttpResponseRedirect(question.get_absolute_url())

@handle404
def profile(request, username = None):
    """Shows a profile page"""
    if username == None:
        user = request.user
    else:
        user = User.objects.get(username = username)
    profile = user.get_profile()
    payload = {'profile':profile, 'user':user }
    return render(request, 'answrs/profile.html', payload)

def create_user(request):
    if request.method == 'POST':
        form = aforms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user = user)
            profile.save()
            from django.contrib.auth import authenticate, login
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            #login(request, user)
            return HttpResponseRedirect('/')
    if request.method == 'GET':
        form = aforms.UserCreationForm()
    payload = {'form':form}
    return render(request, 'registration/create_user.html', payload)

def randompage(request):
    for i in xrange(5):
        count = Question.objects.all().count()
        randcount = random.randint(1, count)
        question = Question.objects.get(id = randcount)
        if question.is_open:
            return HttpResponseRedirect(question.get_absolute_url())
    return HttpResponseRedirect(question.get_absolute_url())
    
def render(request, template, payload):
    all_cat = Category.objects.all()
    open_questions = Question.objects.filter(is_open = True)[:10]
    recently_answered = Question.objects.all().order_by('-latest_answered')[:10]
    payload.update({'all_cat':all_cat, 'open_questions':open_questions, 'recently_answered':recently_answered})
    return render_to_response(template, payload, RequestContext(request))
    
