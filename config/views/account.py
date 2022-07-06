from django.shortcuts import render, redirect, HttpResponse
from config import models
from config.utills import pagination, forms, code
from io import BytesIO
import random


def login(request):
    '''登录'''
    if request.method == "GET":
        form = forms.Accountloginform()
        return render(request, 'login.html', {"forms": form})

    form = forms.Accountloginform(data=request.POST)

    if form.is_valid():
        ##验证码校验
        user_input_code = form.cleaned_data.pop('code')
        str = chr(random.randint(65, 90))
        code_sting = request.session.get('image_code')
        if user_input_code.upper() != code_sting.upper():
            form.add_error('code', "验证码错误")
            return render(request, 'login.html', {"forms": form})

        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", '用户名或密码错误')
            return render(request, 'login.html', {"forms": form})
        ##生成随机字符串，写入到用户的cookie中，再写入session中
        request.session.pop('image_code')
        request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.username}
        ##session保持7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list/')

    return render(request, 'login.html', {"forms": form})


def logout(request):
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    """生成图片验证码"""
    img, code_string = code.check_code()
    ##写入seesion中，以便后续校验
    request.session['image_code'] = code_string
    ##设置超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
