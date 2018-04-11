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
    schema = [("销售", 6500), ("管理", 16000), ("信息技术", 30000), ("客服", 38000), ("研发", 52000), ("市场", 25000)]
    radar = Radar()
    v1 = [[4300, 10000, 28000, 35000, 50000, 19000]]
    v2 = [[5000, 14000, 28000, 31000, 42000, 21000]]
    radar.config(schema)
    radar.add("预算分配", v1, is_splitline=True, is_axisline_show=True)
    radar.add("实际开销", v2, label_color=["#4e79a7"], is_area_show=False)
    radar.show_config()
    return radar
