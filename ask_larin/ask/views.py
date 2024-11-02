from django.shortcuts import render
from django.core.paginator import Paginator
import copy

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
    number = int(request.GET.get("page", 1))
    print("GET page ", number)
    result = {
            "has_previous": False,
            "has_next": False,
        }
    current_page = p.get_page(number)
    print(current_page)
    result["page"] = current_page
    result["current_page"] = current_page.number
    if current_page.has_previous() == True:
        result["has_previous"] = True
        result["previous_page"] = current_page.previous_page_number()
    if current_page.has_next() == True:
        result["has_next"] = True
        result["next_page"] = current_page.next_page_number()
    return result
    try:
        number = int(request.GET.get("page", 1))
        print("GET page ", number)
        result = {
            "has_previous": False,
            "has_next": False,
        }
        current_page = p.get_page(number)
        print(current_page)
        result["page"] = current_page
        result["current_page"] = current_page.number(),
        if current_page.has_previous() == True:
            result["has_previous"] = True
            result["previous_page"] = current_page.previous_page_number()
        if current_page.has_next() == True:
            result["has_next"] = True
            result["next_page"] = current_page.next_page_number()
        return result
    except:
        number = 1
        result = {
            "current_page": number,
            "has_previous": False,
            "has_next": False,
        }
        current_page = p.get_page(number)
        result["page"] = current_page
        if current_page.has_previous():
            result["has_previous"] = True
            result["previous_page"] = current_page.previous_page_number()
        if current_page.has_next():
            result["has_next"] = True
            result["next_page"] = current_page.next_page_number()
        return result


def questions_catalog(request):
    page = paginate(questions, request)
    data = []
    print(page["page"])
    p = tuple(page["page"].object_list)
    print(p)
    for i in range(len(p)):
        data.append({
            "question": p[i],
            "answers_amount": len(answers[p[i]['id']])
        })
    return render(request, 'index.html', {
        'data': data,
        'page': page,
        'login': True
    })

def hot_questions_catalog(request):
    h_q = copy.deepcopy(questions)
    h_q.reverse()
    page = paginate(h_q, request)
    data = []
    p = tuple(page['page'].object_list)
    for i in range(len(p)):
        data.append({
            "question": p[i],
            "answers_amount": len(answers[p[i]['id']])
        })
    return render(request, 'index.html', {
        'data': data,
        'page': page,
        'hot': True
    })

def tag(request, tag):
    data = []
    for i in questions:
        if tag in i['tags']:
            data.append({
                "question": i,
                "answers_amount": len(answers[i['id']])
            })
    page = paginate(data, request)
    return render(request, 'index.html', {
        'data': data,
        'page': page
    })

def question(request, id):
    return render(request, 'question.html', {
        'title': questions[id-1]['title'],
        'question': questions[id-1],
        'answers': answers[id-1]
    })

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'setting.html', {'login': True})

def register(request):
    return render(request, 'register.html')

def new_question(request):
    return render(request, 'new_question.html')