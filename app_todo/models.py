from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.CharField(verbose_name='姓名', max_length=16, db_index=True, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=30)


class Todo(models.Model):
    """
    待办事项
    """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    desc = models.TextField(verbose_name='详情', null=True)
    datetime = models.DateTimeField(verbose_name='时间', max_length=64)
    status = models.CharField(verbose_name='标记', default='0', max_length=10, null=True)
    priority = models.ForeignKey(to='Priority', on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(to='UserInfo', on_delete=models.DO_NOTHING, null=True)


class Priority(models.Model):
    """
    优先级
    """
    pid = models.AutoField(verbose_name='ID', primary_key=True)
    index = models.CharField(verbose_name='优先级', max_length=3, unique=True)