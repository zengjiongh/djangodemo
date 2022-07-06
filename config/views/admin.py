from django.shortcuts import render, redirect
from config import models
from config.utills import pagination, forms

def admin_list(request):
    """管理员列表"""
    ##检查用户是否登录，获取cookie中的session
    info = request.session.get("info")
    if not info:
        return redirect('/login/')


    data_dic = {}
    value = request.GET.get("q","")
    if value:
        data_dic["username_contains"] = value
    queryset = models.Admin.objects.filter(**data_dic)
    page_obj = pagination.Pagination(request, queryset)
    context = {
        "value":value,
        "queryset":page_obj.page_queryset,
        "page_string":page_obj.html()
    }
    return render(request,"admin_list.html",context)

def admin_add(request):
    '''新建管理员'''
    title = "新建管理员"
    if request.method == "GET":
        form = forms.Adminaddform()
        return render(request,"admin_add.html",{"forms":form,"title": title})

    form = forms.Adminaddform(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request,"admin_add.html",{"forms":form,"title": title})

def admin_edit(request,nid):
    '''编辑管理员'''
    title = "新建管理员"
    queryset = models.Admin.objects.filter(id=nid).first()
    if not queryset:
        return render(request,"errors.html",{'error':"数据不存在"})
    if request.method == "GET":
        form = forms.Admineditform(instance=queryset)
        return render(request,"admin_edit.html",{"forms":form,"title": title})
    form = forms.Admineditform(request.POST,instance=queryset)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request,"admin_edit.html",{"forms":form,"title": title})

def admin_delete(request,nid):
    '''删除管理员'''
    queryset = models.Admin.objects.filter(id=nid).first()
    if not queryset:
        return render(request,"errors.html",{'error':"数据不存在"})
    else:
        queryset.delete()
    return redirect('/admin/list/')

def admin_reset(request,nid):
    '''重置密码'''
    queryset = models.Admin.objects.filter(id=nid).first()
    title = "重置密码 - {}".format(queryset.username)
    if not queryset:
        return render(request, "errors.html", {'error': "数据不存在"})
    if request.method == "GET":
        form = forms.Adminresetform()
        return render(request, "admin_edit.html", {"forms": form, "title": title})
    form = forms.Adminresetform(request.POST, instance=queryset)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "admin_edit.html", {"forms": form, "title": title})







