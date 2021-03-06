from django.shortcuts import render, redirect
from compass.models import Results, Answer, Question_choice, Question, Business_Priority, Category
from compass.forms import UserDetailForm, AnswerChoiceForm
import pandas as pd
import json

all_Questions = Question.objects.all()


def home_page(request):
    return render(request, 'home.html')


def new_rmb(request, userdetails):
    rmb_ = Results.objects.create(userdetails=userdetails)
    request.session['rmb_id'] = rmb_.id
    return


def userdetails(request):
    if request.method == "POST":
        form = UserDetailForm(request.POST)
        if form.is_valid():
            userdetails = form.save(commit=False)
            userdetails.first_name = form.cleaned_data['first_name']
            userdetails.last_name = form.cleaned_data['last_name']
            userdetails.email = form.cleaned_data['email']
            userdetails.company = form.cleaned_data['company']
            userdetails.role = form.cleaned_data['role']
            userdetails.save()
            new_rmb(request, userdetails)
            return redirect(f'/rating')
        else:
            return render(request, 'userdetails.html', {'form': form, 'errors': form.errors})

    form = UserDetailForm()
    return render(request, 'userdetails.html', {'form': form})


def get_questions(request, question_id):
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    next_question_id = int(question_id) + 1
    last_question_id = rmb_.quiz.questions.last().id
    all_questions_count = all_Questions.count()

    try:
        question_ = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return render(request, '404.html')

    if request.method == "POST":
        if Question_choice.objects.filter(question_choice=rmb_, question=question_).exists():
            # If the results already exists, we need to update not create a new one
            results_answers = Question_choice.objects.get(question=question_id, question_choice=rmb_)
            form = AnswerChoiceForm(data=request.POST, question_id=question_id, instance=results_answers)
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
            if (next_question_id > last_question_id):
                return redirect(f'/results')
            else:
                return redirect(f'/question/{next_question_id}')

    # Setting the form
    form = AnswerChoiceForm(question_id=question_id)
    # If the question has already been answered
    if Question_choice.objects.filter(question_choice=rmb_, question=question_).exists():
        # If the object exists and the user wants to modify
        results_answers = Question_choice.objects.get(question=question_id, question_choice=rmb_)
        form.fields['answer'].initial = results_answers.answer
        form.fields['comment'].initial = results_answers.comment

    return render(request, 'question.html', {'question': question_, 'rmb': rmb_, 'form': form, 'CountQuestions': all_questions_count})


def results(request):
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    choices = Question_choice.objects.filter(question_choice=rmb)
    answer_array = []
    for c in choices:
        question = Question.objects.get(id = c.question_id)
        answer = Answer.objects.get(description = c.answer)
        answer_array.append({question.category.categoryName: answer.score})
    df = pd.DataFrame(answer_array)
    labels = list(df)
    data = list(df.mean())
    tick_label = json.dumps(labels)
    priorities = Business_Priority.objects.filter(results = rmb)

    materialityData = []
    for priority in priorities:
        materiality = float(priority.score)
        materialityData.append(materiality)

    return render(request, 'results.html', {'maturity': data, 'materiality':materialityData, 'labels': labels, 'tick_label': tick_label})


def rating(request):
    # last_question = request.session['last_question']
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    categories = list(Category.objects.values_list('categoryName', flat=True))
    if request.method == "POST":
        # loop over all the categories and pull out the results and create business priority objects
        for category in categories:
            score = request.POST.get(category)
            actualCategory = Category.objects.get(categoryName = category)
            if Business_Priority.objects.filter(results=rmb_, category= actualCategory).exists():
                edit_business = Business_Priority.objects.get(results=rmb_, category= actualCategory)
                edit_business.score = score
                edit_business.save()
            else:
                business_priority = Business_Priority(category = actualCategory, score = score, results = rmb_)
                business_priority.save()
        return redirect(f'/question/1')
    
    return render(request, 'businessPriority.html', {'categories': categories})
