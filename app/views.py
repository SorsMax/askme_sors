from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': f'Здесь текст вопроса №{i}'
    } for i in range(1, 8)
]

def index(request):
    return render(
        request, 'index.html',
        context={'questions': QUESTIONS}
    )
