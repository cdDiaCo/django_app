from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Poll, Question, Answer, Results

questions_per_page = 5 # Show 5 questions per page

def index(request):
    polls_list = Poll.objects.all()
    context = {
        'polls_list': polls_list,
    }
    return render(request, 'polls_app/index.html', context)


def detail(request, poll_id):
    request.session['validation_passed'] = True
    request.session['current_page'] = 1

    poll = get_object_or_404(Poll, pk=poll_id)
    questions_list = Question.objects.filter(poll_id=poll_id)
    sorted_questions_list = get_sorted_questions(int(request.session['current_page']), questions_list)

    answers = Answer.objects.filter(question__in = sorted_questions_list).select_related()

    total_num_of_pages = int( len(questions_list) / questions_per_page )
    if len(questions_list) % questions_per_page:
        total_num_of_pages += 1
    request.session['total_num_of_pages'] = total_num_of_pages

    #page = request.GET.get('page')

    x = render(request, 'polls_app/poll_detail.html',
                      {'poll': poll, 'sorted_questions': sorted_questions_list, 'answers': answers, 'validation_passed': request.session['validation_passed'],
                       'current_page': request.session['current_page'], 'total_pages': request.session['total_num_of_pages'] })
    request.session['vali']
    return x


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

        if len(answers_list) < questions_per_page: # validation did not pass
            request.session['validation_passed'] = False
        else:
            request.session['current_page'] = int(request.session['current_page']) + 1
            #request.session['validation_passed'] = True


        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        if int(request.session['current_page']) == int(request.session['total_num_of_pages']) and request.session['validation_passed']:
            return HttpResponseRedirect(
                reverse('polls_app:poll_results', args=(poll.id, total_score['answer_score__sum'])))




        poll = get_object_or_404(Poll, pk=poll_id)
        questions_list = Question.objects.filter(poll_id=poll_id)
        #page = request.GET.get('page')


        sorted_questions_list = get_sorted_questions(int(request.session['current_page']), questions_list)
        answers = Answer.objects.filter(question__in=sorted_questions_list).select_related()


        return render(request, 'polls_app/poll_detail.html',
                      {'poll': poll, 'sorted_questions': sorted_questions_list, 'answers': answers,
                       'validation_passed': request.session['validation_passed'], 'current_page': request.session['current_page'],
                       'total_pages': request.session['total_num_of_pages'] })



def get_sorted_questions(current_page, questions_list):
    start_at = current_page * questions_per_page - questions_per_page
    stop_at = current_page * questions_per_page

    sorted_questions_list = []
    for i in range(0, len(questions_list)):
        if i < start_at or i >= stop_at:
            continue

        sorted_questions_list.append(questions_list[i])

    return sorted_questions_list




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








