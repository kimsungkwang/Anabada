import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from Anabada.settings import MEDIA_ROOT

class Main(APIView):
    def get(self, request):

        # select * from content_feed; 역활
        feed_list = Feed.objects.all().order_by('-id')


        return render(request, "Anabada/main.html", context=dict(feeds= feed_list))

class UploadFeed(APIView):
    def post(self, requset):

        # 파일 불러오기
        file = requset.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        name = requset.data.get("name")
        price = requset.data.get("price")
        content = requset.data.get("content")
        user_id = requset.data.get("user_id")
        profile_image = requset.data.get("profile_image")

        Feed.objects.create(image=image, name=name, price=price, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200)