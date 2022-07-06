from django.shortcuts import render, redirect, HttpResponse
from config import models
from config.utills import pagination, forms
import pandas as pd


def depart_list(request):
    """  部门列表 """
    data_list = {}
    value = request.GET.get("q", "")
    if value:
        data_list["title__contains"] = value
    queryset = models.Department.objects.filter(**data_list)
    page_obj = pagination.Pagination(request, queryset)
    content = {
        "value": value,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    return render(request, 'depart_list.html', content)


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    ##获取值
    depart = request.POST.get("depart")
    print(depart)
    ## 保存到数据库
    models.Department.objects.create(title=depart)
    ## 重定向回部门列表
    return redirect('/depart/list')


def depart_delete(request):
    """ 删除部门 """

    ##获取id
    nid = request.GET.get("nid")
    # 删除
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list')


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        depart = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"depart": depart})
    new_depart = request.POST.get("new_depart")
    models.Department.objects.filter(id=nid).update(title=new_depart)
    return redirect("/depart/list")


def depart_multi(request):
    file_object = request.FILES.get("exc")
    df = pd.read_excel(file_object)
    de_list = df["部门"]
    for depart in de_list:
        exits = models.Department.objects.filter(title=depart).exists()
        if not exits:
            models.Department.objects.create(title=depart)
    return redirect('/depart/list')
