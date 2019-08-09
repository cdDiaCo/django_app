from django.test import TestCase

from polls_app.views import calculateNecessaryAnswers
from .models import Poll, Question, Answer



class NecessaryAnswersTests(TestCase):
    pass

    def setUp(self):
        Poll.objects.create(poll_name="Ancient History Test", poll_description="Description of Ancient History Test")
        poll = Poll.objects.get(poll_name="Ancient History Test")

        for i in range(1, 11):
            question_text = "Question number " + str(i)
            Question.objects.create(question_text=question_text, poll_id=poll.id)
            question = Question.objects.get(question_text=question_text)
            for j in range(1, 4):
                answer_text = "Answer number " + str(i) + "." + str(j)
                answer_score = 10 * j
                Answer.objects.create(answer_text=answer_text, answer_score=answer_score, question_id=question.id)

        #Poll.objects.create(poll_name="Middle Ages History Test", poll_description="Description of Middle Ages History Test")


    def test_poll_with_many_pages(self):
        poll = Poll.objects.get(poll_name="Ancient History Test")
        total_pages = 3
        score_difference = 20
        self.assertIs(calculateNecessaryAnswers(poll.id, total_pages, score_difference), [])



