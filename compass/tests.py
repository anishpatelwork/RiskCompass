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
