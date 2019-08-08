from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Poll, Question, Answer, Results

questions_per_page = 3 # Show 3 questions per page


def index(request):
    polls_list = Poll.objects.all()
    context = {
        'polls_list': polls_list,
    }
    return render(request, 'polls_app/index.html', context)



def detail(request, poll_id):
    if 'current_page' not in request.session:
        request.session['current_page'] = 1

    if 'answers_received' not in request.session:
        request.session['answers_received'] = []

    if 'validation_passed' not in request.session:
        request.session['validation_passed'] = True

    poll = get_object_or_404(Poll, pk=poll_id)
    questions_list = Question.objects.filter(poll_id=poll_id)

    if 'total_num_of_pages' not in request.session:
        request.session['total_num_of_pages'] = getNumOfPages(questions_list)

    current_page_questions = get_current_page_questions(int(request.session['current_page']), questions_list)
    request.session['current_page_questions_number'] = len(current_page_questions)
    answers = Answer.objects.filter(question__in = current_page_questions).select_related()

    x = render(request, 'polls_app/poll_detail.html',
                      {'poll': poll, 'current_page_questions': current_page_questions, 'answers': answers, 'validation_passed': request.session['validation_passed'],
                       'current_page': request.session['current_page'], 'total_pages': request.session['total_num_of_pages'] })

    request.session['validation_passed'] = True # reset validation flag to initial value

    return x

def getNumOfPages(questions_list):
    total_num_of_pages = len(questions_list) // questions_per_page # get only integer(not float) from division
    if len(questions_list) % questions_per_page > 0:
        total_num_of_pages += 1

    return total_num_of_pages


def submit(request, poll_id):
    poll = get_object_or_404(Question, pk=poll_id)

    answers_received = request.POST.getlist('answer')
    questions_list = Question.objects.filter(poll_id=poll_id)

    current_page_questions = get_current_page_questions(int(request.session['current_page']), questions_list)
    validation = isPageValid(answers_received, current_page_questions)

    if not validation: # validation did not pass
        request.session['validation_passed'] = False
        return HttpResponseRedirect(
            reverse('polls_app:poll_detail', args=(poll.id,)))

    else: # validation passed
        for answer in answers_received:
            # store the answers received after every page in a session variable
            request.session['answers_received'].append(answer.split(".")[0])


        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.
        if int(request.session['current_page']) == int(request.session['total_num_of_pages']):
            total_score = Answer.objects.filter(pk__in=request.session['answers_received']).aggregate(Sum('answer_score'))
            del request.session['current_page']

            return HttpResponseRedirect(
                reverse('polls_app:poll_results', args=(poll.id, total_score['answer_score__sum'])))

        else:
            request.session['current_page'] = int(request.session['current_page']) + 1
            return HttpResponseRedirect(reverse('polls_app:poll_detail', args=(poll.id,)))



def isPageValid(answers_received, current_page_questions):
    answered_questions = getAnsweredQuestions(answers_received)

    for question in current_page_questions:
        if question.id not in answered_questions:
            return False

    return True



def getAnsweredQuestions(answers_received):
    questions_received = []
    for answer in answers_received:
        questions_received.append(int(answer.split(".")[1]))

    return  questions_received



def get_current_page_questions(current_page, questions_list):
    start_at = current_page * questions_per_page - questions_per_page
    stop_at = current_page * questions_per_page

    current_page_questions = []
    for i in range(0, len(questions_list)):
        if i < start_at or i >= stop_at:
            continue

        current_page_questions.append(questions_list[i])

    return current_page_questions




def results(request, poll_id, total_score):
    poll = get_object_or_404(Poll, pk=poll_id)
    db_results = Results.objects.filter(poll_id = poll_id)
    upper_limit = getUpperLimit(db_results, total_score)

    max_possible_score = False
    necessary_answers = []


    if isMaxPossibleScore(poll_id, upper_limit[1]):
        max_possible_score = True
    else:
        score_difference = upper_limit[1] - total_score
        necessary_answers = calculateNecessaryAnswers(poll_id, int(request.session['total_num_of_pages']), score_difference)


    del request.session['total_num_of_pages']
    x = render(request, 'polls_app/poll_results.html', { 'poll': poll, 'total_score':total_score, 'upper_limit': upper_limit[1], 'result_id': upper_limit[0],
                                                         'necessary_amswers': necessary_answers, 'max_possible_score': max_possible_score })

    del request.session['answers_received']
    return x


# needs implementation !!!
def isMaxPossibleScore(poll_id, upper_limit):
    result = Results.objects.filter(poll_id = poll_id).order_by('-result_upper_limit').first()

    if result.result_upper_limit == upper_limit :
        return True

    return False





def calculateNecessaryAnswers(poll_id, total_pages, score_difference):
    questions_list = Question.objects.filter(poll_id=poll_id)
    necessary_answers = []

    for page_num in range(1, total_pages+1): # select only one answer for every page
        current_page_questions = get_current_page_questions(page_num, questions_list)

        # order answers by score desc
        answers = Answer.objects.filter(question__in=current_page_questions).select_related().order_by('-answer_score')

        for answer in answers:
            if answer.answer_score > score_difference : # in this case only one answer is needed to change the result

                if len(necessary_answers) > 0 :
                    # the list already has other answers with smaller score (from previous pages)
                    # empty the list. Previously added elements are no longer necessary
                    while len(necessary_answers) > 0:
                        necessary_answers.pop()

                necessary_answers.append(answer)
                return necessary_answers
            else: # score_difference is too big, more answers are needed to change the result
                score_sum = sum(int(answer.answer_score) for answer in necessary_answers)
                if score_sum <= score_difference : # already added answers are not enough, more answers needed
                    necessary_answers.append(answer)
                    break # jump to the next page - outer for
                else: # sum of already added answers are enough to change the result
                    return necessary_answers

    return []



def getUpperLimit(results, total_score):
    upper_limit_list = []

    for result in results:
        if total_score > result.result_upper_limit:
            continue
        else:
            upper_limit_list.append((result.id, result.result_upper_limit))

    upper_limit = min(upper_limit_list, key=lambda x: x[1])

    return upper_limit