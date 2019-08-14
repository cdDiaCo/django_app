from django.test import TestCase

import polls_app.views
from polls_app.views import calculateNecessaryAnswers
from .models import Poll, Question, Answer



class NecessaryAnswersTests(TestCase):

    def setUp(self):
        poll = Poll.objects.create(poll_name="Ancient History Test", poll_description="Description of Ancient History Test")

        for i in range(1, 11): # 10 questions
            question_text = "Question number " + str(i)
            question = Question.objects.create(question_text=question_text, poll_id=poll.id)
            for j in range(1, 4): # 3 answers for every question
                answer_text = "Answer number " + str(i) + "." + str(j)
                answer_score = 10 * j
                Answer.objects.create(answer_text=answer_text, answer_score=answer_score, question_id=question.id)


        #Poll.objects.create(poll_name="Middle Ages History Test", poll_description="Description of Middle Ages History Test")


    def test_poll_with_few_pages_and_big_score_difference(self):
        # import pdb;
        # pdb.set_trace()
        polls_app.views.questions_per_page = 5
        poll = Poll.objects.get(poll_name="Ancient History Test")
        answers_received = ['3.1.1', '6.2.1', '9.3.1', '12.4.1', '15.5.1', '18.6.2', '21.7.2', '24.8.2', '27.9.2', '30.10.2'] # format: [answer_id].[question_id].[page]
        total_pages = 2
        score_difference = 100
        necessary_answers_two = calculateNecessaryAnswers(poll.id, total_pages, score_difference, answers_received)
        self.assertEqual(necessary_answers_two, [])


    def test_poll_with_many_pages_and_big_score_difference(self):
        # import ipdb;ipdb.set_trace(context=25)
        polls_app.views.questions_per_page = 3
        poll = Poll.objects.get(poll_name="Ancient History Test")
        answers_received = ['33.1.1', '36.2.1', '39.3.1', '42.4.2', '45.5.2', '48.6.2', '51.7.3', '54.8.3', '57.9.3', '60.10.4'] # format: [answer_id].[question_id].[page]
        total_pages = 4
        score_difference = 100
        necessary_answers_one = calculateNecessaryAnswers(poll.id, total_pages, score_difference, answers_received)
        self.assertEqual(necessary_answers_one, [])



    def test_poll_with_many_pages_and_small_score_diference(self):
        polls_app.views.questions_per_page = 3
        poll = Poll.objects.get(poll_name="Ancient History Test")
        answers_received = ['63.1.1', '66.2.1', '69.3.1', '72.4.2', '75.5.2', '78.6.2', '81.7.3', '84.8.3', '87.9.3', '90.10.4']  # format: [answer_id].[question_id].[page]
        total_pages = 4
        score_difference = 20
        necessary_answers_three = calculateNecessaryAnswers(poll.id, total_pages, score_difference, answers_received)
        score_sum = 30
        for answer in necessary_answers_three:
            score_sum += answer.answer_score

        self.assertIs(score_sum > score_difference, True)
















