from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.utills import forms, pagination
from config import models
import json
import random
from datetime import datetime


@csrf_exempt
def order_list(request):
    form = forms.OrderModelform()
    queryset = models.Order.objects.all().order_by("-id")
    obj_page = pagination.Pagination(request, queryset)
    context = {
        "forms": form,
        "queryset": obj_page.page_queryset,
        "page_string": obj_page.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单 Ajax"""
    form = forms.OrderModelform(data=request.POST)
    if form.is_valid():
        # 固定设置管理员ID
        form.instance.admin_id = request.session["info"]["id"]
        ## 生成随机订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.save()
        data_string = {"status": True}
        return HttpResponse(json.dumps(data_string))
    data_sting = {"status": False, "errors": form.errors}
    return JsonResponse(data_sting)


@csrf_exempt
def order_delete(request):
    nid = request.POST.get("nid")
    exist = models.Order.objects.filter(id=nid).exists()
    if not exist:
        return JsonResponse({"status": False, "errors": "数据不存在"})

    models.Order.objects.filter(id=nid).delete()
    data_string = {"status": True, }
    return JsonResponse(data_string)


@csrf_exempt
def order_detail(request):
    nid = request.POST.get("nid")
    row_dict = models.Order.objects.filter(id=nid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "errors": "数据不存在"})

    return JsonResponse({"status": True, "data": row_dict})


@csrf_exempt
def order_edit(request):
    nid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=nid).first()
    if not row_dict:
        return JsonResponse({"status": False, "tips": "数据不存在"})
    form = forms.OrderModelform(data=request.POST, instance=row_dict)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "errors": form.errors})
