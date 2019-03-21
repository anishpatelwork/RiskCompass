from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from compass.models import RMB
from compass.forms import UserDetailsForm
import math

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def new_rmb(request):
    rmb_ = RMB.objects.create()
    request.session['rmb_id'] = rmb_.id
    return redirect(f'/userdetails')

def userdetails(request):
    rmb_id = request.session['rmb_id']
    rmb_ = RMB.objects.get(id=rmb_id)
    if request.method == "POST":
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            userdetails = form.save(commit =False)
            userdetails.first_name = request.POST.get("first_name", "")
            userdetails.last_name = request.POST.get("last_name","")
            userdetails.email = request.POST.get("email","")
            userdetails.company = request.POST.get("company","")
            userdetails.role = request.POST.get("role","")
            userdetails.sector = request.POST.get("sector", "")
            userdetails.rmb = rmb_
            userdetails.save()
            return redirect(f'/question/1')
    else:
        form = UserDetailsForm()
        return render(request, 'userdetails.html', {'form': form})

def question(request, question_id):
    rmb_id = request.session['rmb_id']
    rmb_ = RMB.objects.get(id=rmb_id)
    question_ = rmb_.quiz.questions.get(id=question_id)
    return render(request, 'question.html', {'question': question_, 'rmb': rmb_})


def answer(request, question_id, answer_id):
    print(question_id)
    next_question_id = int(question_id) + 1
    print(next_question_id)
    rmb_id = request.session['rmb_id']
    rmb = RMB.objects.get(id=rmb_id)
    rmb.add_answer(question_id, answer_id)
    last_question_id = rmb.quiz.questions.last().id
    if(next_question_id > last_question_id):
        return redirect(f'/results')
    else:
        return redirect(f'/question/{next_question_id}')


def results(request):
    rmb_id = request.session['rmb_id']
    rmb = RMB.objects.get(id=rmb_id)
    data = rmb.get_answer_score_array()
    recommendations = rmb.get_recommendations()
    print(recommendations)
    return render(request, 'results.html', {'data': data, 'recommendations': recommendations})
