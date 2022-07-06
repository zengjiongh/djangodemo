from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from config.utills import forms,pagination
from config import models
import json


def task_list(request):
    queryset = models.Task.objects.all().order_by("-id")
    form = forms.Taskform()
    obj_page = pagination.Pagination(request,queryset)
    context = {
        "forms": form,
        "queryset": obj_page.page_queryset,
        "page_string":obj_page.html()
    }
    return render(request, "task_list.html",context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_sting = {"status": True, "data": [11, 35, 565, 757]}
    json_sting = json.dumps(data_sting)
    return HttpResponse(json_sting)


@csrf_exempt
def task_add(request):
    print(request.POST)
    form = forms.Taskform(data=request.POST)
    if form.is_valid():
        form.save()
        data_sting = {"status": True}
        return HttpResponse(json.dumps(data_sting))
    data_dict = {"status":False,"error":form.errors}
    return HttpResponse(json.dumps(data_dict))
