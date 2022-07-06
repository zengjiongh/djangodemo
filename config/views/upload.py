import os.path

from django.shortcuts import render, HttpResponse,redirect
from config.utills import forms
from config import models


def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    # print(request.POST)
    # print(request.FILES)
    file_obj = request.FILES.get("avaturo")
    # print(file_obj)
    with open(file_obj.name, mode="wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse("...")


def upload_form(request):
    title = "Form上传文件"
    if request.method == "GET":
        form = forms.UpForm()
        return render(request, "upload_form.html", {"forms": form, "title": title})
    form = forms.UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        img_object = form.cleaned_data["img"]
        media_dir = os.path.join("media", "boss", img_object.name)
        with open(media_dir, mode="wb") as f:
            for chunk in img_object.chunks():
                f.write(chunk)

        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=media_dir,
        )
        return HttpResponse("上传成功")
    return render(request, "upload_form.html", {"forms": form, "title": title})


def upload_modelform(request):
    title = "ModelForm上传"
    if request.method == "GET":
        form = forms.CityModelForm()
        return render(request, "upload_form.html", {"forms": form, "title": title})

    form = forms.CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_form.html", {"forms": form, "title": title})

