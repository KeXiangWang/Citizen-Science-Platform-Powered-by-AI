from django.db import models

from User.models import UserInfo
from django.utils import timezone
from os.path import basename

class DomainInfo(models.Model):
    """ 数据领域信息

    Attributes:
        aid           领域id 主键
        domain_name   领域名称
    """
    aid = models.IntegerField(verbose_name='领域ID', primary_key=True)
    domain_name = models.CharField(verbose_name='领域名', max_length=40)

    def __str__(self):
        return self.domain_name


class ModelInfo(models.Model):
    """ 判别模型信息

    Attributes:
        mid                   模型编号 主键
        model_name            模型名称
        model_introduction    模型介绍
        is_unloaded           是否用户自定义
        model_path            模型路径
    """
    mid = models.IntegerField(verbose_name='模型ID', primary_key=True)
    model_name = models.CharField(verbose_name='模型名字', max_length=30)
    model_introduction = models.TextField(verbose_name='模型介绍', max_length=5000)
    is_unloaded = models.BooleanField(verbose_name='自定义与否', default=False)
    model_path = models.CharField(verbose_name='模型路径', max_length=256)


class ProjectInfo(models.Model):
    """ 项目信息

    Attributes:
        pid                     项目id 主键
        projection_name         项目名称
        projection_introduction 项目介绍
        publisher               项目发布者 UserInfo外键 项目发布人信息不变 发布人信息只是用来展示
        publish_time            项目发布时间
        area                    项目领域 DomainInfo外键 项目的领域删除后 其中所有的项目均删除
        model                   项目检测模型 ModelInfo外键 模型删除后 项目的模型信息置为空
        projection_image        项目缩略图路径
    """
    pid = models.IntegerField(verbose_name='项目ID', primary_key=True)
    projection_name = models.CharField(verbose_name='项目名字', max_length=100)
    projection_introduction = models.TextField(verbose_name='项目介绍', max_length=5000)
    publisher = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, blank=True, null=True)
    publish_time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)
    # FIXME change /auto_now_add=True/ -> /default=timezone.now/ by wkx, check whether safe.
    area = models.ForeignKey(DomainInfo, on_delete=models.CASCADE)
    model = models.CharField(verbose_name='模型路径', max_length=256, default='null')
    projection_image = models.CharField(verbose_name='项目缩略图', max_length=256, null=True)
    need_data = models.CharField(verbose_name='项目所需数据', max_length=4096, null=True)

    def __str__(self):
        return self.projection_name


class DataInfo(models.Model):
    """ 数据信息

    Attributes:
        data_id   数据id 主键
        data_type 数据类型
        data_name 数据名称
        data_path 数据路径
        time      数据上传时间
        user_id   上传用户id
    """
    data_id = models.IntegerField(verbose_name='上传数据ID', primary_key=True)
    data_type = models.CharField(verbose_name='数据类型', max_length=256)
    data_name = models.CharField(verbose_name='数据名称', max_length=256)
    data_path = models.CharField(verbose_name='数据路径', max_length=256)
    data_location = models.CharField(verbose_name='数据上传位置', blank=True,null=True,max_length=256)
    data_province = models.CharField(verbose_name='数据上传省份', blank=True,null=True,max_length=256)
    data_time = models.DateTimeField(verbose_name='数据上传时间', default=timezone.now)
    uid = models.ForeignKey('User.UserInfo', on_delete=models.SET_NULL, blank=True, null=True)  # 用户删除，数据仍然保留

    def __str__(self):
        return self.data_name


class ProjectImage(models.Model):
    """ 项目数据对应关系

    Attributes:
        pid       项目id ProjectInfo外键
        data_id   数据id DataInfo外键
        verified  审核情况  0：未审核   1：审核为有效数据   2：审核为无效数据
    """
    pid = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    data_id = models.ForeignKey(DataInfo, on_delete=models.CASCADE)
    verified = models.IntegerField(verbose_name='审核情况', default=0)

    def __str__(self):
        return '{}_{}'.format(self.pid, self.data_id)


class UserProjectAuthority(models.Model):
    """ 用户权限

    Attributes:
        uid         用户id UserInfo外键 用户删除后，项目用户对应关系删除
        pid         项目id ProjectInfo外键 项目删除后，项目用户对应关系删除
        authority   数据权限 0:administrator 1:publisher 2:manger 3:volunteer_joined
    """
    uid = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    pid = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    register_time = models.DateTimeField(verbose_name='权限登记时间', default=timezone.now)
    authority = models.IntegerField(verbose_name='用户参与权限', default=3)

    def __str__(self):
        return '{}_{}'.format(self.uid, self.pid)


class IssueInfo(models.Model):
    """ 项目帖子

    Attributes:
        issue_id    issue的id
        uid         issue的提出者
        title       issue的题目
        description issue提出的待解答的问题
        time        issue发布的时间
    """
    issue_id = models.IntegerField(verbose_name='issueID', primary_key=True)
    uid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(verbose_name='issue题目', max_length=100)
    description = models.CharField(verbose_name='issue问题描述', max_length=280)
    time = models.DateTimeField(verbose_name='issue发布时间', auto_now_add=True)

    def __str__(self):
        return self.title


class CommentInfo(models.Model):
    issue_id = models.ForeignKey(IssueInfo, on_delete=models.CASCADE)
    uid = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(verbose_name='评论内容', max_length=100)
    time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)


class ProjectIssue(models.Model):
    pid = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    issue_id = models.ForeignKey('IssueInfo', on_delete=models.CASCADE)
