from django.shortcuts import render, redirect
from compass.models import Results
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
    rmb_id = request.session['rmb_id']
    rmb_ = Results.objects.get(id=rmb_id)
    question_ = rmb_.quiz.questions.get(id=question_id)
    return render(request, 'question.html', {'question': question_, 'rmb': rmb_})


def answer(request, question_id, answer_id):
    next_question_id = int(question_id) + 1
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    rmb.add_answer(question_id, answer_id)
    last_question_id = rmb.quiz.questions.last().id
    if(next_question_id > last_question_id):
        return redirect(f'/results')
    else:
        return redirect(f'/question/{next_question_id}')


def results(request):
    rmb_id = request.session['rmb_id']
    rmb = Results.objects.get(id=rmb_id)
    data = rmb.get_answer_score_array()
    recommendations = rmb.get_recommendations()
    return render(request, 'results.html', {'data': data, 'recommendations': recommendations})
