""" Tests file for the compass app. """
from django.test import TestCase
from django.urls import resolve
from compass.views import home_page
from compass.models import Results, Quiz, UserDetails

# Create your tests here.


class HomePageTest(TestCase):
    """ Tests Home page. """
    def test_root_url_resolves_to_home_page_view(self):
        """ Tests root url. """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        """ Tests the home template returns. """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewRMBTest(TestCase):
    """ Tests creating a new result. """
    #def test_redirects_after_POST(self):
     #   response = self.client.post('/rmb/new', data={})
      #  new_rmb = Results.objects.first()
       # self.assertRedirects(response, f'/question/1')

    def test_new_rmb_contains_quiz_and_empty_answers(self):
        """ Tests the new result contains quiz and answers. """
        user = UserDetailsTest.create_user_details()
        new_rmb = Results.objects.create(userdetails=user)
        self.assertEqual(new_rmb.quiz.questions.count(), 10)
        self.assertEqual(new_rmb.answer_list, '{}')


#class RMBModelTest(TestCase):
 #   def test_get_answer_integer_array_returns_integers(self):
  #      user = UserDetailsTest.create_user_details(self)
   #     rmb = Results.objects.create(userdetails=user)
    #    rmb.add_answer(1, 4)
     #   rmb.add_answer(2, 8)
      #  rmb.add_answer(3, 12)
       # results = rmb.get_answers_integer_array()
        #expectedResults = [4, 8, 12]
        #self.assertCountEqual(results, expectedResults)
        #sum = 0
        #for result in results:
         #   sum = sum + result
        #self.assertEqual(sum, 24)


class QuizModelTest(TestCase):
    """ Tests the quiz model. """
    def test_quiz_contains_ten_questions(self):
        """ Tests the quiz contains questions. """
        quiz = Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)

class UserDetailsTest(TestCase):
    """ Tests user details model. """

    @classmethod
    def create_user_details(cls):
        """ Creates a user detail. """
        useremail = 'temp@temp.com'
        user = UserDetails.objects.create(email=useremail)
        return user

    def test_user_had_email(self):
        """ Tests the user has email. """
        useremail = 'temp@temp.com'
        user = self.create_user_details()
        self.assertEqual(user.email, useremail)

class AnswerTest(TestCase):
    """ Tests the answers. """
    def test_answer_redirects_to_next_question(self):
        """ Tests the answers redirect to next answer. """
        user = UserDetailsTest.create_user_details()
        rmb = Results.objects.create(userdetails=user)
        session = self.client.session
        session['rmb_id'] = rmb.id
        session.save()
        response = self.client.post('/question/1/answer/1')
        self.assertRedirects(response, f'/question/2')

    def test_answer_redirects_last_question_to_results(self):
        """ Tests the last answers redirect to results. """
        user = UserDetailsTest.create_user_details()
        rmb = Results.objects.create(userdetails=user)
        session = self.client.session
        session['rmb_id'] = rmb.id
        session.save()
        last_question = rmb.quiz.questions.last().id
        response = self.client.post(f'/question/{last_question}/answer/1')
        self.assertRedirects(response, f'/results')

    #def test_answer_adds_answer_to_answer_list(self):
     #   """ Tests the answers add answer to list. """
      #  session = self.client.session
       # session['rmb_id'] = 1
        #session.save()
        #user = UserDetailsTest.create_user_details(self)
       #rmb = Results.objects.create(userdetails=user)
       # self.assertEquals(rmb.answer_list, '{}')
        #response = self.client.post('/question/1/answer/1')
        #rmb = Results.objects.get(id=1)
        #self.assertEquals(rmb.answer_list, '{"1": "1"}')
        #response = self.client.post('/question/2/answer/5')
        #rmb = Results.objects.get(id=1)
        #self.assertEquals(rmb.answer_list, '{"1": "1", "2": "5"}')
