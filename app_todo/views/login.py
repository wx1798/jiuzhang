from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.response import Response
from ast import literal_eval  # 将字符串转成字典
from app_todo.util.hash_pwd import hashpwd
from app_todo.models import UserInfo
import uuid
from app_todo.util.email import sender_code


class AuthView(ViewSetMixin, APIView):
    def login(self, request, *args, **kwargs):
        print(request.data.get('username'), '------')
        ret = {'code': 1000}
        username = request.data.get('username')
        password = request.data.get('password')
        # 查缓存 解码 转成字典
        # exists_user = literal_eval(redis_server().get(username).decode("utf-8"))
        hash_password= hashpwd(password)
        exists_user = cache.get(username)
        if exists_user and exists_user[0] == hash_password and exists_user[2] != 0:
            ret['token'] = exists_user[1]
            return Response(ret)
        # 可以去掉
        else:
            user = UserInfo.objects.filter(user=username, password=hash_password).filter()
            if not user:
                ret['code'] = 1001
                ret['error'] = "用户名密码错误"
            else:
                # 存在 直接存入缓存之中(密码, token, 登入状态)
                uid = str(uuid.uuid4())
                ret['token'] = uid
                # redis_server().set(username, [password, uid, 1], 60*60*6)
                cache.set(username, [hash_password, uid, 1], 60 * 60 * 6)
        return Response(ret)

    def register(self, request, *args, **kwargs):
        ret = {'code': 1000}
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        check_code = request.data.get("checkCode")
        if check_code == cache.get("jwt"+username):
            if username and password:
                UserInfo.objects.create(user=username, password=hashpwd(password), email=email)
                ret['path'] = '/login/'
                return Response(ret)
        ret['code'] = 3002
        ret['data'] = 'error'
        return Response(ret)

    def send(self, request, *args, **kwargs):
        ret = {'code': 1000}
        username = request.data.get("username")
        email = request.data.get("email")
        is_success = sender_code(email)
        if is_success:
            ret['data'] = "请注意查收"
            cache.set('jwt'+username, is_success)
        else:
            ret['code'] = 1001
            ret['data'] = "邮箱错误"
        return Response(ret)