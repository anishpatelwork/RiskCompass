from django.shortcuts import render, redirect
from compass.models import Results, Answer, Question_choice, Question, Business_Priority
from compass.forms import UserDetailForm, AnswerChoiceForm, BusinessPriorityForm
import pandas as pd

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
            return redirect(f'/question/1')
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
                return redirect(f'/rating')
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
    # scores = {}
    answer_array = []
    for c in choices:
        question = Question.objects.get(id = c.question_id)
        # print(question.category)
        answer = Answer.objects.get(description = c.answer)
        answer_array.append({question.category.categoryName: answer.score})

    df = pd.DataFrame(answer_array)
    labels = list(df)
    data = list(df.mean())
    return render(request, 'results.html', {'data': data, 'labels': labels})


def rating(request):
    last_question = request.session['last_question']
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    if request.method == "POST":
        # Check if editing or not
        if Business_Priority.objects.filter(results=rmb_).exists():
            priority = Business_Priority.objects.get(results=rmb_)
            form = BusinessPriorityForm(data=request.POST, instance=priority)
        else:
            form = BusinessPriorityForm(request.POST)
        if form.is_valid():
            business_priority = form.save(commit=False)
            business_priority.data_quality = rating_helpfunc(int(form.cleaned_data['data_quality']))
            business_priority.cat_modeling = rating_helpfunc(int(form.cleaned_data['cat_modeling']))
            business_priority.non_modelled = rating_helpfunc(int(form.cleaned_data['non_modelled']))
            business_priority.profiling_submissions = rating_helpfunc(int(form.cleaned_data['profiling_submissions']))
            business_priority.results = rmb_
            business_priority.save()
            return redirect(f'/results')

    form = BusinessPriorityForm()
    return render(request, 'businessPriority.html', {'form': form, 'last_question': last_question})


def rating_helpfunc(priority_number):
    if priority_number == 1:
        return 'Low'
    elif priority_number ==2:
        return 'Medium'
    else:
        return 'High'
