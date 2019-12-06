from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from app_todo.models import Todo, Priority, UserInfo
import time
from rest_framework.viewsets import GenericViewSet, ViewSetMixin


class TodoSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    priority = serializers.CharField(source='priority.index')
    user = serializers.CharField(source='user.user')

    class Meta:
        model = Todo
        fields = ['desc', 'status', 'priority', 'datetime', 'user']   # 查询全部 '__all__'
        # depth = 1  # 根据关联字段找到表序列化2层（0-10）
        # exclude = ('add_time',):  除去指定的某些字段


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
        date = request.data.get("date")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def update(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("date")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def add(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("date")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def delete(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("date")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def filter(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("msg")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)

    def all(self, request, *args, **kwargs):
        ret = {"code": 1000, "data": None}
        username = request.data.get("username")
        token = request.data.get("token")
        date = request.data.get("date")
        datetime = date.split('-')
        queryset = Todo.objects.filter(user__user=username, datetime__year=datetime[0], datetime__month=datetime[1],
                                       datetime__day=datetime[2])
        serializers_msg = TodoSerializer(instance=queryset, many=True)
        ret["data"] = serializers_msg.data
        return Response(ret)