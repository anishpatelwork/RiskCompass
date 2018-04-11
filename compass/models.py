from django.db import models
import json


class Quiz(models.Model):
    name = "Quiz"


class RMB(models.Model):
    quiz = Quiz.objects.first()
    answer_list = models.TextField(default='{}')

    def add_answer(self, question_id, answer_id):
        answers = json.loads(self.answer_list)
        answers[question_id] = answer_id
        self.answer_list = json.dumps(answers)
        self.save()


class Question(models.Model):
    description = models.TextField(default='')
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)


class Answer(models.Model):
    description = models.TextField(default='')
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
