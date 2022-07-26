import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed, Like, Reply, Bookmark
from Anabada.settings import MEDIA_ROOT


class Main(APIView):
    def get(self, request):

        # 세션 --> 로그인 을 한 후 다른 웹 사이트 갔다 와도 그대로 저장 , 로그 아웃 하면 정보들 날라감
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        # select * from content_feed; 역활
        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        # 유저 테이블은 프로필 사진 변경할 때 자동으로 실시간으로 갱신되기 때문에 글을 쓰고나서 프로필을 바꿔도 예전에 쓴 글에 프로필 사진이 바뀐다.
        # 사용자 정보를 아예 id로 넣어 두는게 실시간으로 데이터 바뀌는 것을 반영할 수 있다.
        # 글을 쓰는 순간에 프로필 이미지와 닉네임은 고정된 값
        # id 를 넣는게 시간을 변경된 데이터를 보여 줄 때 더 좋다.
        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(name=feed.name,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  price=feed.price,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list,
                                  id=feed.id,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))

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
        email = request.session.get('email', None)

        Feed.objects.create(image=image, name=name, price=price, content=content, email=email)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):

        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        print(like_list)

        return render(request, "content/profile.html", context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)
