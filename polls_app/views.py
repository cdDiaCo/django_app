from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Poll, Question, Answer, Results



def index(request):
    polls_list = Poll.objects.all()
    context = {
        'polls_list': polls_list,
    }
    return render(request, 'polls_app/index.html', context)


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions_list = Question.objects.filter(poll_id=poll_id)
    answers = Answer.objects.filter(question__in = questions_list).select_related()

    paginator = Paginator(questions_list, 5)  # Show 5 questions per page

    page = request.GET.get('page')
    questions = paginator.get_page(page)

    return render(request, 'polls_app/poll_detail.html', {'poll': poll, 'questions': questions, 'answers': answers})


def submit(request, poll_id):
    poll = get_object_or_404(Question, pk=poll_id)
    try:
        answers_list = request.POST.getlist('answer')
    except (KeyError, Answer.DoesNotExist):  # THIS NEEDS TO BE CHANGED!
        # Redisplay the question voting form.
        return render(request, 'polls_app/poll_detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })
    else:
        total_score = Answer.objects.filter(pk__in=answers_list).aggregate(Sum('answer_score'))


        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls_app:poll_results', args=(poll.id, total_score['answer_score__sum'])))



def results(request, poll_id, total_score):
    poll = get_object_or_404(Poll, pk=poll_id)
    results = Results.objects.filter(poll_id = poll_id).filter()

    upper_limit_list = []

    for result in results:
        if total_score > result.result_upper_limit :
            continue
        else:
            upper_limit_list.append((result.id, result.result_upper_limit))

    upper_limit = min(upper_limit_list, key=lambda  x:x[1])

    return render(request, 'polls_app/poll_results.html', {'poll': poll, 'total_score':total_score, 'upper_limit': upper_limit[1], 'result_id': upper_limit[0] })








