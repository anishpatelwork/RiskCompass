from django.db import models

# Create your models here.


class RMB(models.Model):
    pass


class Quiz(models.Model):
    pass


class Question(models.Model):
    description = models.TextField(default='')
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)


class Answer(models.Model):
    description = models.TextField(default='')
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
