from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from compass.models import RMB
from pyecharts import Radar
import math

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def new_rmb(request):
    rmb_ = RMB.objects.create()
    return redirect(f'/rmb/{rmb_.id}/question/1')


def question(request, rmb_id, question_id):
    rmb_ = RMB.objects.get(id=rmb_id)
    question_ = rmb_.quiz.questions.get(id=question_id)
    return render(request, 'question.html', {'question': question_, 'rmb': rmb_})


def answer(request, rmb_id, question_id, answer_id):
    next_question_id = int(question_id) + 1
    rmb = RMB.objects.get(id=rmb_id)
    rmb.add_answer(question_id, answer_id)
    last_question_id = rmb.quiz.questions.last().id
    if(next_question_id > last_question_id):
        return redirect(f'/rmb/{rmb_id}/results')
    else:
        return redirect(f'/rmb/{rmb_id}/question/{next_question_id}')


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def results(request, rmb_id):
    template = loader.get_template('results.html')
    rmb = RMB.objects.get(id=rmb_id)
    l3d = radar()
    context = dict(
        myechart=l3d.render_embed(),
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


def radar():
    schema = [("Data Quality", 5), ("Cat Modeling", 5), ("Non Modeled", 5), ("Profiling Submissions", 5), ("Pricing", 5), ("Binding", 5), ("Capacity Management", 5), ("Risk Transfer", 5), ("Event Response", 5), ("Reporting", 5)]
    radar = Radar()
    v1 = [[3, 2, 2, 5, 3, 5, 3, 5, 1, 4]]
    radar.config(schema, shape="polygon")
    radar.add("Results", v1, is_legend_show=False, is_label_show=False, is_toolbox_show=False)
    return radar
