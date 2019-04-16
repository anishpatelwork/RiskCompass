from django.db import models
import json, datetime

DEFAULT_QUIZ_ID = 1

class Quiz(models.Model):
    name = models.TextField(default='Exceedance', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Quiz"


class Question(models.Model):
    category = models.TextField(default='')
    description = models.TextField(default='')
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)

    # Set the name for the title of the questions
    def __str__(self):
        return self.category

class Answer(models.Model):
    description = models.TextField(default='')
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    recommendation = models.TextField(default='Contact Anish Patel for more information')

    def __str__(self):
        return self.description

class UserDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return ("%s %s" %(self.last_name, self.email))

    class Meta:
        verbose_name_plural = "User Details"

class Results(models.Model):
    userdetails = models.OneToOneField(UserDetails, related_name='results', on_delete=models.CASCADE, default=DEFAULT_QUIZ_ID)
    quiz = models.ForeignKey(Quiz, related_name='quizresults', on_delete=models.CASCADE, default = DEFAULT_QUIZ_ID)
    answer_list = models.TextField(default='{}')
    date = models.DateField(default=datetime.date.today)

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
            if (answer.score < 5):
                question = Question.objects.get(id=q_id)
                returnDict[question] = answer.recommendation
        return returnDict

        # Rename it for the plural state

    class Meta:
        verbose_name_plural = "Results"

    def __str__(self):
        return ("Quiz %s" % (self.date))