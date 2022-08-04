import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed
from Anabada.settings import MEDIA_ROOT


class Main(APIView):
    def get(self, request):

        # select * from content_feed; 역활
        feed_list = Feed.objects.all().order_by('-id')

        # 세션 --> 로그인 을 한 후 다른 웹 사이트 갔다 와도 그대로 저장 , 로그 아웃 하면 정보들 날라감
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        return render(request, "Anabada/main.html", context=dict(feeds=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        # 파일 불러오기
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        name = request.data.get("name")
        price = request.data.get("price")
        content = request.data.get("content")
        user_id = request.data.get("user_id")
        profile_image = request.data.get("profile_image")

        Feed.objects.create(image=image, name=name, price=price, content=content, user_id=user_id,
                            profile_image=profile_image, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):

        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        return render(request, "content/profile.html", context=dict(user=user))
