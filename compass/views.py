""" The views for Compass app. """
import json
import pandas as pd
from django.shortcuts import render, redirect

from compass.forms import UserDetailForm, AnswerChoiceForm
from compass.models import Results, Answer, QuestionChoice, Question, \
    BusinessPriority, Category, UserDetails

ALL_QUESTIONS = Question.objects.all()

def home_page(request):
    """ Renders the homepage. """
    return render(request, 'home.html')


def new_rmb(request, userdetails):
    """ Creates a new Result for the session. """
    rmb_ = Results.objects.create(userdetails=userdetails)
    request.session['rmb_id'] = rmb_.id


def user_details(request):
    """ Handles the User detail input. """
    if request.method == "POST":
        form = UserDetailForm(request.POST)
        if form.is_valid():
            userdetails_form = form.save(commit=False)
            userdetails_form.first_name = form.cleaned_data['first_name']
            userdetails_form.last_name = form.cleaned_data['last_name']
            userdetails_form.email = form.cleaned_data['email']
            userdetails_form.company = form.cleaned_data['company']
            userdetails_form.role = form.cleaned_data['role']
            userdetails_form.save()
            new_rmb(request, userdetails_form)
            return redirect(f'/rating')
        return render(request, 'userdetails.html', {'form': form, 'errors': form.errors})

    form = UserDetailForm()
    return render(request, 'userdetails.html', {'form': form})


def get_questions(request, question_id):
    """ Handles the User detail input. """
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    next_question_id = int(question_id) + 1
    last_question_id = rmb_.quiz.questions.last().id
    all_questions_count = ALL_QUESTIONS.count()

    try:
        question_ = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return render(request, '404.html')

    if request.method == "POST":
        if QuestionChoice.objects.filter(question_choice=rmb_, question=question_).exists():
            results_answers = QuestionChoice.objects.get(
                question=question_id,
                question_choice=rmb_
            )
            form = AnswerChoiceForm(
                data=request.POST,
                question_id=question_id,
                instance=results_answers
            )
        else:
            form = AnswerChoiceForm(data=request.POST, question_id=question_id)
        if form.is_valid():
            answer_choice = form.save(commit=False)
            answer_choice.comment = form.cleaned_data['comment']
            answer_choice.answer = form.cleaned_data['answer']
            answer_choice.question = question_
            answer_choice.question_choice = rmb_
            answer_choice.save()
            request.session['last_question'] = question_id
            if next_question_id > last_question_id:
                return redirect(f'/results')
            return redirect(f'/question/{next_question_id}')

    # Setting the form
    form = AnswerChoiceForm(question_id=question_id)
    # If the question has already been answered
    if QuestionChoice.objects.filter(question_choice=rmb_, question=question_).exists():
        # If the object exists and the user wants to modify
        results_answers = QuestionChoice.objects.get(question=question_id, question_choice=rmb_)
        form.fields['answer'].initial = results_answers.answer
        form.fields['comment'].initial = results_answers.comment

    return render(request, 'question.html', {'question': question_, 'rmb': rmb_,
                                             'form': form, 'CountQuestions': all_questions_count})


def results(request):
    """ Renders and calculates the results. """
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    choices = QuestionChoice.objects.filter(question_choice=rmb)
    answer_array = []
    for choice in choices:
        question = Question.objects.get(id=choice.question_id)
        answer = Answer.objects.get(description=choice.answer)
        answer_array.append({question.category.categoryName: answer.score})
    data_frame = pd.DataFrame(answer_array)
    labels = list(data_frame)
    data = list(data_frame.mean())
    tick_label = json.dumps(labels)
    priorities = BusinessPriority.objects.filter(results=rmb)

    materiality_data = []
    for priority in priorities:
        materiality_data.append(float(priority.score))

    return render(request, 'results.html',
                  {
                      'maturity': data,
                      'materiality':materiality_data,
                      'labels': labels,
                      'tick_label': tick_label
                  }
                  )


def rating(request):
    """ Renders and processes the ratings. """
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    categories = list(Category.objects.values_list('categoryName', flat=True))
    if request.method == "POST":
        # loop over all the categories and pull out the results and create business priority objects
        for category in categories:
            score = request.POST.get(category)
            actual_category = Category.objects.get(categoryName=category)
            if BusinessPriority.objects.filter(results=rmb_, category=actual_category).exists():
                edit_business = BusinessPriority.objects.get(results=rmb_, category=actual_category)
                edit_business.score = score
                edit_business.save()

            business_priority = BusinessPriority(
                category=actual_category,
                score=score,
                results=rmb_
            )
            business_priority.save()
        return redirect(f'/question/1')
    return render(request, 'businessPriority.html', {'categories': categories})


def login(request):
    """ Checks if a user has already taken the quiz and renders. """
    if request.method == "POST":
        email = request.POST.get('result_email')
        if UserDetails.objects.filter(email=email).exists():
            user = UserDetails.objects.get(email=email)
            user_results = Results.objects.get(userdetails=user)
            # This is the only hack about it. Changing the rmb_id in the request session
            # But the user can't change anything anyway
            request.session['rmb_id'] = user_results.id
            return redirect(f'/results')

        message = 'There is no result available for this email: %s' % email
        return render(request, 'login.html', {'error_message': message})
    return render(request, 'login.html')
