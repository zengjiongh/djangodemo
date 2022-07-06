from django.shortcuts import render, redirect
from config import models
from config.utills import pagination, forms


# Create your views here.




def user_list(request):
    """ 用户管理 """
    data_list = {}
    value = request.GET.get("q", "")
    if value:
        data_list["name__contains"] = value
    queryset = models.UserInfo.objects.filter(**data_list)
    page_obj = pagination.Pagination(request,queryset)

    content = {
        "user_list":page_obj.page_queryset,
        "page_string":page_obj.html(),
        'value': value
    }

    """
    python获取数据
    时间格式create_time.strftime("%Y-%m-%d")转字符串
    obj.depart.title获取外键对应值
    obj.get_gender_display()获取数字对应值
    for obj in query:
        print(obj.create_time.strftime("%Y-%m-%d"),obj.depart.title,obj.depart_id,obj.get_gender_display())
    """
    return render(request, "user_list.html", content)


def user_add(request):
    """ 添加用户 """
    if request.method == "GET":
        gender_choice = models.UserInfo.gender_choice
        depart = models.Department.objects.all()
        return render(request, "user_add.html", {"departs": depart, "gender": gender_choice})

    ##获取用户数据
    user = request.POST.get("name")
    password = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("account")
    time = request.POST.get("time")
    depart = request.POST.get("depart")
    gender = request.POST.get("gender")

    ##添加到数据库中
    models.UserInfo.objects.create(name=user, password=password,
                                   age=age, account=account,
                                   create_time=time, depart_id=depart, gender=gender)
    ##返回到用户列表界面

    return redirect("/user/list")


def user_model_form_adds(request):
    """ 添加用户（基于ModelForm版本） """
    if request.method == "GET":
        form = forms.Useraddform()
        return render(request, "user_model_form_adds.html", {"forms": form})

    ##用户提交数据，数据的校验
    form = forms.Useraddform(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # form.save()将数据保存到数据库
        form.save()
        return redirect('/user/list')

    ##校验失败
    return render(request, 'user_model_form_adds.html', {"forms": form})


def user_edit(request, nid):
    """ 编辑用户 """
    ##根据ID去数据库获取要编辑的那行数据
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        ##instance获取数据
        form = forms.Useraddform(instance=row_object)
        return render(request, "user_edit.html", {"forms": form})

    form = forms.Useraddform(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入的所有值，如果想要在后台增加其他字段
        ## form.instance.字段名=值
        form.save()
        return redirect("/user/list")
    return render(request, 'user_edit.html', {"forms": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")