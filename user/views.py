import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Anabada.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password


class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, requset):
        # TODO 회원가입
        email = requset.data.get('email', None)
        password = requset.data.get('password', None)
        name = requset.data.get('name', None)
        nickname = requset.data.get('nickname', None)

        User.objects.create(email=email,
                            password=make_password(password),
                            name=name,
                            nickname=nickname,
                            profile_image='default_profile.jpeg')

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원 정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원 정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):

        # 세션 지우기
        request.session.flush()
        return render(request, 'user/login.html')

class UploadProfile(APIView):
    def post(self, request):

        # 파일 불러오기
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)

