from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import copy

from .forms import LoginForm

# Create your views here.
TAGS = [
    {
        'tag_name': f'black-jack'
    },
    {
        'tag_name': f'bender'
    }
]

ASKS = [
    {
        'text': f'Здесь текст ответа №{i}',
        'is_editable': True if i % 3 == 0 else False,
        'is_correct': True if i % 2 == 0 else False
    } for i in range(1, 21)
]

QUESTIONS = [
    {
        'title': f'Вопрос №{i}',
        'id': i,
        'text': f'Здесь текст вопроса №{i}',
        'tags': TAGS,
        'asks': ASKS
    } for i in range(1, 81)
]

def paginate(objects_list, request, per_page=10):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page

def index(request):
    try:
        page = paginate(QUESTIONS, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def hot(request):
    QUESTIONS_DESCR = copy.deepcopy(QUESTIONS)
    QUESTIONS_DESCR.reverse()
    try:
        page = paginate(QUESTIONS_DESCR, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def tag(request, tag_name):
    try:
        page = paginate(QUESTIONS, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'tag.html',
        context={'questions': page.object_list, 'page_obj': page, 'tag_name': tag_name}
    )

def question(request, question_id):
    try:
        question = QUESTIONS[question_id-1]
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    page = paginate(question['asks'], request, 4)

    return render(
        request, 'question.html',
        context={'question': question, 'asks': page.object_list, 'page_obj': page}
    )

def signin(request):

    is_error = False
    error_text = ''

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/')
        else:
            if form.data['password'] == '':
                error_text = 'Sorry, empty password!'
                is_error = True
            if form.data['login'] == '':
                error_text = 'Sorry, empty login!'
                is_error = True
    else:
        form = LoginForm()

    return render(
        request, 'signin.html',
        context={'form': form, 'is_error': is_error, 'error_text': error_text}
    )

def signup(request):

    return render(
        request, 'signup.html',
        context={}
    )
