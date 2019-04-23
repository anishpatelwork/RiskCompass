from django.shortcuts import render, redirect
from compass.models import Results, Answer, Question_choice, Question
from compass.forms import UserDetailForm


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

def question(request, question_id):
    # Need to get the result answer and if null just return the question
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    question = Question.objects.get(id=question_id)
    question_ = rmb_.quiz.questions.get(id=question_id)
    if Question_choice.objects.filter(question_choice=rmb_, question= question).exists():
        # If the object exists and the user wants to modify
        results_answers = Question_choice.objects.get(question=question_id)
        return render(request, 'question.html', {'question': question_, 'rmb': rmb_, 'answer': results_answers})

    return render(request, 'question.html', {'question': question_, 'rmb': rmb_})


# Create a form for each of the questions. Validate here and add to results with comments
def answer(request, question_id, answer_id):
    # get the result_answer with the question id
    # if empty return empty and new form
    # else return all items with selected and comment
    next_question_id = int(question_id) + 1
    rmb_id = request.session['rmb_id']
    answer = Answer.objects.get(id=answer_id)
    question = Question.objects.get(id=question_id)
    rmb = Results.objects.get(id=rmb_id)

    if Question_choice.objects.filter(question_choice=rmb, question= question).exists():
        # If the object exists and the user wants to modify
        Question_choice.objects.filter(question=question).update(answer = answer)
    else:
        Question_choice.objects.create(question = question, answer = answer, question_choice = rmb)

    # Need the comment to add here as well
    # rmb.add_answer(question_id, answer_id, 'Temp for now')
    last_question_id = rmb.quiz.questions.last().id
    if(next_question_id > last_question_id):
        return redirect(f'/results')
    else:
        return redirect(f'/question/{next_question_id}')


def results(request):
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    choices = Question_choice.objects.filter(question_choice=rmb)
    answer_array = []
    #data = rmb.get_answer_score_array()
    for c in choices:
        answer = Answer.objects.get(description = c.answer)
        answer_array.append(answer.score)
    return render(request, 'results.html', {'data': answer_array})
