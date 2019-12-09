from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from app_todo.models import Todo, Priority, UserInfo
import time
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from functools import wraps


def decorate(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.data.get("username")
        token = request.data.get("token")
        message = cache.get(user)
        if user and message[1] == token:
            return func(self, request, *args, **kwargs)
        ret = {"code": 4000, "error": "msg error"}
        return Response(ret)

    return wrapper


class TodoSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    priority = serializers.CharField(source='priority.index')
    user = serializers.CharField(source='user.user')

    class Meta:
        model = Todo
        fields = ['id', 'desc', 'status', 'priority', 'datetime', 'user']   # 查询全部 '__all__'
        # depth = 1  # 根据关联字段找到表序列化2层（0-10）
        # exclude = ('add_time',):  除去指定的某些字段


class TimeSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    priority = serializers.CharField(source='priority.index')
    user = serializers.CharField(source='user.user')
    key = serializers.CharField(source='id')

    class Meta:
        model = Todo
        fields = ['key', 'desc',  'priority', 'datetime']   # 查询全部 '__all__'
        # depth = 1  # 根据关联字段找到表序列化2层（0-10）
        # exclude = ('add_time',):  除去指定的某些字段


class HomeSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    index = serializers.CharField(source='priority.index')
    key = serializers.CharField(source='id')

    class Meta:
        model = Todo
        fields = ['key', 'desc',  'index', 'status', 'datetime']   # 查询全部 '__all__'


class HomeView(ViewSetMixin, APIView):
    def home(self, request, *args, **kwargs):
        """
        首页
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("datetime")
        queryset = Todo.objects.filter(user__user=username)
        serializers_msg = HomeSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def today(self, request, *args, **kwargs):
        """
        今天
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("datetime")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        # serializers_msg = TodoSerializer(instance=queryset, many=True)
        # ret["data"] = serializers_msg.data
        # return Response(ret)
        if queryset:
            serializers_msg = HomeSerializer(instance=queryset, many=True)
            ret["data"] = serializers_msg.data
        else:
            ret["code"] = 4000
        return Response(ret)

    def update(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        status = request.data.get("status")
        tid = request.data.get("tid")
        datetime = request.data.get("datetime")
        desc = request.data.get("desc")
        index = request.data.get("index")
        index_obj = Priority.objects.get(index=index)
        Todo.objects.filter(id=tid).update(desc=desc, status=status, datetime=datetime, priority=index_obj)
        return Response(ret)

    def add(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        desc = request.data.get("desc")
        date = request.data.get("datetime")
        index = request.data.get("index")
        status = request.data.get("status")
        user_obj = UserInfo.objects.get(user=username)
        index_obj = Priority.objects.get(index=index)
        add_obj = Todo.objects.create(user=user_obj, desc=desc, datetime=date, status=0, priority=index_obj)
        data = {"key": add_obj.id, "desc": add_obj.desc, "status": add_obj.status, "datetime": add_obj.datetime, "index": add_obj.priority.index}
        ret["data"] = data
        return Response(ret)

    def delete(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("date")
        tid = request.data.get("tid")
        Todo.objects.filter(id=tid).delete()
        return Response(ret)

    def filter(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        index = request.data.get("index")
        queryset = Todo.objects.filter(user__user=username, priority__index=index).order_by("datetime")
        if queryset:
            serializers_msg = HomeSerializer(instance=queryset, many=True)
            ret["data"] = serializers_msg.data
        else:
            ret["code"] = 4000
        return Response(ret)

    def all(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        queryset = Todo.objects.filter(user__user=username)
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def find(self, request, *args, **kwargs):
        msg = request.data.get("msg")
        return

    def init(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        date = request.data.get("datetime")
        username = request.data.get("username")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        if queryset:
            serializers_msg = HomeSerializer(instance=queryset, many=True)
            ret["data"] = serializers_msg.data
        else:
            ret["code"] = 4000
        return Response(ret)
