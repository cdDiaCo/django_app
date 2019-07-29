from django.db import models

# Create your models here.


class Poll(models.Model):
    poll_name = models.CharField(max_length=200)
    poll_description = models.CharField(max_length=500)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
    answer_score = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text


class Results(models.Model):
    result_text = models.CharField(max_length=500)
    result_upper_limit = models.IntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return  self.result_text



    