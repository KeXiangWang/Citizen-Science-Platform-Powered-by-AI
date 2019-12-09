from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """ 用户信息

    Attributes:
            uid                 用户id,主键
            password            密码，MD5cd
            credit              用户信用值
            register_date       注册时间
            user_name           用户姓名
            sex                 用户性别
            user_introduction   用户简介
            age                 年龄
            email_address       邮箱地址
    """
    uid = models.BigAutoField(verbose_name='用户ID', primary_key=True)  # 用户ID，主键
    password = models.CharField(verbose_name='密码', max_length=256)  # 存MD5加密后内容
    credit = models.IntegerField(verbose_name='信誉', default=50)  # 上限 100，低于0账号被封禁
    register_date = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    user_name = models.CharField(verbose_name='用户姓名', max_length=20)
    sex = models.BooleanField(verbose_name='用户性别', null=True, blank=True)
    user_introduction = models.TextField(verbose_name='用户自我介绍', max_length=2000)
    age = models.IntegerField(verbose_name='用户年龄', default=0, null=True, blank=True)
    email_address = models.EmailField(verbose_name='邮箱')
    avatar = models.CharField(verbose_name='头像路径', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user_name


class UnauthorizedUserInfo(models.Model):
    """ 待验证用户信息

    Attributes:
            uid                 用户id,主键
            email_address       邮箱地址
            authorization       验证码
            pre_register_date   登记时间
    """
    uid = models.BigAutoField(verbose_name='用户ID', primary_key=True)
    email_address = models.EmailField(verbose_name='邮箱', max_length=128)
    authorization = models.CharField(verbose_name='验证码', max_length=6)
    pre_register_date = models.DateTimeField(verbose_name='登记时间', auto_now=True)  # 登记时间为发送最近一次验证码的时间

    def __str__(self):
        return self.email_address


class UserVisitRecord(models.Model):  # 这是对应关系，其中一项删除后，该关系就删除
    """ 用户浏览项目表

    Attributes:
            uid           用户id,外键
            pid           项目id,外键
            visit_times   浏览次数
    """
    uid = models.ForeignKey('User.UserInfo', on_delete=models.CASCADE)
    pid = models.ForeignKey('Project.ProjectInfo', on_delete=models.CASCADE)  # 均级联删除
    visit_times = models.IntegerField(verbose_name='该用户访问此项目次数', default=1)


