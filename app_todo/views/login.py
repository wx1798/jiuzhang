from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from ast import literal_eval  # 将字符串转成字典
from app_todo.util.hash_pwd import hashpwd
from app_todo.models import UserInfo
import uuid


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
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