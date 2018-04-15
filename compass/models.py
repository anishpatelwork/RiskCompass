from django.db import models
import json


class Quiz(models.Model):
    pass


DEFAULT_QUIZ_ID = 1


class RMB(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='rmb', on_delete=models.CASCADE, default=DEFAULT_QUIZ_ID)
    answer_list = models.TextField(default='{}')

    def add_answer(self, question_id, answer_id):
        answers = json.loads(self.answer_list)
        answers[question_id] = answer_id
        self.answer_list = json.dumps(answers)
        self.save()

    def get_answers_integer_array(self):
        answers = json.loads(self.answer_list)
        returnArray = []
        for key, value in answers.items():
            returnArray.append(int(value))
        return returnArray

    def get_answer_score_array(self):
        answers = json.loads(self.answer_list)
        returnArray = []
        for q_id, a_id in answers.items():
            answer = Answer.objects.get(id=a_id)
            returnArray.append(answer.score)
        return returnArray

    def get_recommendations(self):
        answers = json.loads(self.answer_list)
        returnDict = {}
        for q_id, a_id in answers.items():
            answer = Answer.objects.get(id=a_id)
            if(answer.score < 5):
                question = Question.objects.get(id=q_id)
                returnDict[question] = answer.recommendation
        return returnDict


class Question(models.Model):
    category = models.TextField(default='')
    description = models.TextField(default='')
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)


class Answer(models.Model):
    description = models.TextField(default='')
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    recommendation = models.TextField(default='Contact Anish Patel for more information')
