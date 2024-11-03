from django.shortcuts import render
from django.core.paginator import Paginator
import copy
from ask.models import *
from django.db.models import *

questions = []
for i in range(1,30):
  questions.append({
    'title': 'title' + str(i),
    'id': i,
    'text': 'text' + str(i),
    'tags': ['tag'+str(i), 'tag'+str(i+1), 'tag'+str(i+2)]
  })

answers = []
for i in range(30):
    answers.append([])
    for j in range(5):
        answers[i].append({
        'id': i*5 + j,
        'text': 'text' + str(i*5 + j)
        })



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
    return render(request, 'question.html', {
        'title': question.title,
        'question': question,
        'answers': answers
    })

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'setting.html', {'login': True})

def register(request):
    return render(request, 'register.html')

def new_question(request):
    return render(request, 'new_question.html')