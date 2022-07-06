from django.shortcuts import render, HttpResponse, redirect
from config.utills import forms, pagination
from config import models
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def city_list(request):
    value = request.GET.get('q', "")
    data_dict = {}
    if value:
        data_dict["city__contains"] = value
    queryset = models.City.objects.filter(**data_dict)
    page_obj = pagination.Pagination(request, queryset)
    form = forms.CityModelForm()
    context = {
        "value": value,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "forms": form
    }
    return render(request, "city_list.html", context)


@csrf_exempt
def city_add(request):
    title = "新建"
    if request.method == "GET":
        form = forms.CityModelForm()
        return render(request, "upload_form.html", {"forms": form, "title": title})
    form = forms.CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_form.html", {"forms": form, "title": title})
