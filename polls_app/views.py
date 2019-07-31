from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from .models import Poll, Question, Answer


def index(request):
    polls_list = Poll.objects.all()
    context = {
        'polls_list': polls_list,
    }
    return render(request, 'polls_app/index.html', context)


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = Question.objects.filter(poll_id=poll_id)
    answers = Answer.objects.filter(question__in = questions).select_related()
    return render(request, 'polls_app/poll_detail.html', {'poll': poll, 'questions': questions, 'answers': answers})


