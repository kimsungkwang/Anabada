from django.db import models


# Create your models here.
class Feed(models.Model):
    # 상품 명
    name = models.TextField()
    # 상품 설명
    content = models.TextField()
    # 상품 사진
    image = models.TextField()
    # 상품 가격
    price = models.IntegerField()
    # 글쓴이
    email = models.EmailField()


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    # 찜한 유저
    email = models.EmailField()
    # 눌렀는지 안눌렀는지
    is_like = models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField()
    reply_content = models.TextField()


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField()
    is_marked = models.BooleanField(default=True)
