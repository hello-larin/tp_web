import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from ask.models import *
from django.db.models import *

from .forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, 10)
    try:
        number = int(request.GET.get("page", 1))
        if number > p.num_pages + 1 or number < 1:
            raise Exception()
        current_page = p.get_page(number)
    except:
        number = 1
        current_page = p.get_page(number)
    result = {
            "has_previous": False,
            "has_next": False,
    }
    result["page"] = current_page
    result["current_page"] = current_page.number
    if current_page.has_previous() == True:
        result["has_previous"] = True
        result["previous_page"] = current_page.previous_page_number()
    if current_page.has_next() == True:
        result["has_next"] = True
        result["next_page"] = current_page.next_page_number()
    return result


def questions_catalog(request):
    question = Question.objects.new_questions()
    page = paginate(question, request)
    return render(request, 'index.html', {
        'data': page["page"].object_list,
        'page': page,
        'login': True,
        'new': True
    })

def hot_questions_catalog(request):
    question = Question.objects.hot_questions()
    page = paginate(question, request)
    return render(request, 'index.html', {
        'data': page["page"].object_list,
        'page': page,
        'hot': True,
    })

def tag(request, tag):
    question = Question.objects.tag_questions(tag)
    page = paginate(question, request)
    return render(request, 'index.html', {
        'data': page["page"].object_list,
        'page': page,
        'tag': tag
    })

def question(request, id):
    answers = Answer.objects.question_answers(id)
    question = Question.objects.get(id=id)
    form = AnswerForm()
    return render(request, 'question.html', {
        'title': question.title,
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required(login_url='login')
def answer(request, id):
    question = get_object_or_404(Question, id=id)
    answers = Answer.objects.question_answers(id)
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            form.save(profile=profile, question=question)
            form = AnswerForm()
    return render(request, 'question.html', {
        'title': question.title,
        'question': question,
        'answers': answers,
        'form': form
    })

def login(request):
    next_url = request.GET.get('next', reverse('questions'))
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(next_url)
            else:
                form.add_error(None, 'Неверный логин или пароль')
    return render(request, 'login.html', {
        'form': form,
        'next_url': next_url
    })

@login_required(login_url='login')
def settings(request):
    form = SettingsForm(instance=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()  
    return render(request, 'setting.html', {'form': form})

def logout(request):
    auth.logout(request)
    current_url = request.META.get('HTTP_REFERER', '/')
    return redirect(current_url)

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('questions'))
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def new_question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            question = form.save(profile=profile)
            return redirect('question',question.id)
    return render(request, 'new_question.html', {'form': form})

def question_like(request, id):
    try:
        data = json.loads(request.body)
        print("data loaded")
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    user = request.user
    if user == None:
        return JsonResponse({"error": "No auth"}, status=400)
    rating = QuestionLike.objects.like(id, user, data["rating"])
    print("RATING: ", rating)
    return JsonResponse({"rating" : rating})


def answer_like(request, id):
    try:
        data = json.loads(request.body)
        print("data loaded")
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    user = request.user
    if user == None:
        return JsonResponse({"error": "No auth"}, status=400)
    print(id, user, data["rating"])
    rating = AnswerLike.objects.like(id, user, data["rating"])
    return JsonResponse({"rating" : rating})

def correct_answer(request, id):
    user = request.user
    answer = Answer.objects.get(id=id)
    creator = answer.question.profile.user
    if user != creator:
        return JsonResponse({"error": "No question author"}, status=400)
    answer.correct = not answer.correct
    answer.save()
    return JsonResponse({"status": "OK"}, status=200)