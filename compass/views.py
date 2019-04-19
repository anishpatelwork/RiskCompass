from django.shortcuts import render, redirect
from compass.models import Results, Answer, Question_choice, Question
from compass.forms import UserDetailForm, AnswerChoiceForm


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
            # Getting the first name with the get... Saves it and then redirects
            userdetails.first_name = form.cleaned_data['first_name']
            userdetails.last_name = form.cleaned_data['last_name']
            userdetails.email = form.cleaned_data['email']
            userdetails.company = form.cleaned_data['company']
            userdetails.role = form.cleaned_data['role']
            userdetails.sector = form.cleaned_data['sector']
            userdetails.save()
            new_rmb(request, userdetails)
            return redirect(f'/question/1')

    form = UserDetailForm()
    return render(request, 'userdetails.html', {'form': form})


def get_questions(request, question_id):
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    next_question_id = int(question_id) + 1

    last_question_id = rmb_.quiz.questions.last().id

    if (next_question_id > last_question_id):
        return redirect(f'/results')

    try:
        question_ = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return render(request, '404.html')

    if request.method == "POST":
        form = AnswerChoiceForm(data=request.POST, question_id=question_id)
        if form.is_valid():
            answer_choice = form.save(commit=False)
            answer_choice.comment = form.cleaned_data['comment']
            answer_choice.answer = form.cleaned_data['answer']
            answer_choice.question = question_
            answer_choice.question_choice = rmb_
            answer_choice.save()
            return redirect(f'/question/{next_question_id}')

    # Setting the form
    form = AnswerChoiceForm(question_id=question_id)

    # If the question has already been answered
    if Question_choice.objects.filter(question_choice=rmb_, question=question_).exists():
        # If the object exists and the user wants to modify
        results_answers = Question_choice.objects.get(question=question_id, question_choice=rmb_)
        form.fields['answer'].initial = results_answers.answer
        form.fields['comment'].initial = results_answers.comment

    return render(request, 'question.html', {'question': question_, 'rmb': rmb_, 'form': form})


def results(request):
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    choices = Question_choice.objects.filter(question_choice=rmb)
    answer_array = []
    for c in choices:
        answer = Answer.objects.get(description = c.answer)
        answer_array.append(answer.score)
    return render(request, 'results.html', {'data': answer_array})
