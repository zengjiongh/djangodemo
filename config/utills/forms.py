from django import forms
from config import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from config.utills import bootstrap, encrypt

'''用户'''


class Useraddform(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


'''靓号'''


class Prettyaddform(bootstrap.BootStrapModelForm):
    ##验证方式一(字段+正则)
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误")]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"选择所有字段
        # exclude = ["level"]排除某个字段
        # fields = "__all__"

    # 验证方式二(clean_字段名)钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        ##判断是否重复
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("手机格式错误")
        return txt_mobile


class Prettyeditform(bootstrap.BootStrapModelForm):
    # mobile = forms.CharField(disabled=True)

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        ##当前编辑那一行的ID
        nid = self.instance.pk
        ##判断是否重复
        exists = models.PrettyNum.objects.exclude(id=nid).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("手机格式错误")
        return txt_mobile


'''管理员'''


class Adminaddform(bootstrap.BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", 'password', "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        exit = models.Admin.objects.filter(username=txt_username).exists()
        if exit:
            raise ValidationError("用户名已存在")

        return txt_username

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class Admineditform(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        nid = self.instance.pk
        exit = models.Admin.objects.exclude(id=nid).filter(username=txt_username).exists()
        if exit:
            raise ValidationError("用户名已存在")
        return txt_username


class Adminresetform(bootstrap.BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        nid = self.instance.pk
        md5_pwd = encrypt.md5(pwd)
        exit = models.Admin.objects.filter(id=nid, password=md5_pwd).exists()
        if exit:
            raise ValidationError("不允许与原密码一样")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


'''登录'''


class Accountloginform(bootstrap.BootStrapForm):
    username = forms.CharField(
        label="用户名",
        max_length=32,
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True)
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput
    )

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        md5_pwd = encrypt.md5(pwd)
        return md5_pwd


'''任务列表'''


class Taskform(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            'detail': forms.TextInput
        }


class OrderModelform(bootstrap.BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid", "admin"]


"""上传文件"""


class UpForm(bootstrap.BootStrapForm):
    bootstrap_exclude_fields = ["img"]
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="图片")


class CityModelForm(bootstrap.BootStrapModelForm):
    bootstrap_exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"
