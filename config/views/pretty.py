from django.shortcuts import render, redirect
from config import models
from config.utills import pagination, forms


# Create your views here.






def pretty_list(request):
    """ 靓号列表 """
    data_list = {}
    value = request.GET.get("q", "")
    if value:
        data_list["mobile__contains"] = value
    queryset = models.PrettyNum.objects.filter(**data_list).order_by('-level')


    page_obj = pagination.Pagination(request,queryset)
    content = {
        "value": value,
        "queryset":page_obj.page_queryset,
        "page_string":page_obj.html()

    }
    return render(request, 'pretty_list.html',content)


def pretty_add(request):
    """ 靓号添加 """
    if request.method == "GET":
        form = forms.Prettyaddform()
        return render(request, 'pretty_add.html', {"forms": form})

    form = forms.Prettyaddform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {"forms": form})


def pretty_edit(request, nid):
    """ 靓号编辑 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = forms.Prettyeditform(instance=row_object)
        return render(request, "pretty_edit.html", {"forms": form})
    form = forms.Prettyeditform(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"forms": form})


def pretty_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")