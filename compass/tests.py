from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from compass.views import home_page
from compass.models import RMB, Quiz

# Create your tests here.


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewRMBTest(TestCase):
    def test_redirects_after_POST(self):
        response = self.client.post('/rmb/new', data={})
        new_rmb = RMB.objects.first()
        self.assertRedirects(response, f'/rmb/{new_rmb.id}/question/1')

    def test_new_rmb_contains_quiz_and_empty_answers(self):
        response = self.client.post('/rmb/new', data={})
        new_rmb = RMB.objects.first()
        self.assertEqual(new_rmb.quiz.questions.count(), 10)
        self.assertEqual(new_rmb.answer_list, '{}')


class QuizModelTest(TestCase):

    def test_quiz_contains_ten_questions(self):
        quiz = Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)


class AnswerTest(TestCase):

    def test_answer_redirects_to_next_question(self):
        rmb = RMB.objects.create()
        response = self.client.post('/rmb/1/question/1/answer/1')
        self.assertRedirects(response, f'/rmb/1/question/2')

    def test_answer_redirects_last_question_to_results(self):
        rmb = RMB.objects.create()
        last_question = rmb.quiz.questions.last().id
        response = self.client.post(f'/rmb/1/question/{last_question}/answer/1')
        self.assertRedirects(response, f'/rmb/1/results')

    def test_answer_adds_answer_to_answer_list(self):
        rmb = RMB.objects.create()
        self.assertEquals(rmb.answer_list, '{}')
        response = self.client.post('/rmb/1/question/1/answer/1')
        rmb = RMB.objects.get(id=1)
        self.assertEquals(rmb.answer_list, '{"1": "1"}')
        response = self.client.post('/rmb/1/question/2/answer/5')
        rmb = RMB.objects.get(id=1)
        self.assertEquals(rmb.answer_list, '{"1": "1", "2": "5"}')
