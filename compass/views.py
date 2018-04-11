from django.shortcuts import render, redirect
from compass.models import RMB

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def new_rmb(request):
    rmb_ = RMB.objects.create()
    return redirect(f'/rmb/{rmb_.id}/question/1')


def question(request, rmb_id, question_id):
    return render(request, 'question.html')
