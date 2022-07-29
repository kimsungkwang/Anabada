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
    # 유저 아이디
    user_id = models.TextField()
    # 프로필 이미지
    profile_image = models.TextField()
    # 찜 수
    like_count = models.IntegerField()
