from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from compass.models import RMB
import math

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def new_rmb(request):
    rmb_ = RMB.objects.create()
    request.session['rmb_id'] = rmb_.id
    return redirect(f'/question/1')


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
    return render(request, 'results.html', {'data': data})
