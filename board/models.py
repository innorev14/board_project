from django.db import models

# Create your models here.
'''
2. 모델 document - author, cartegory,title, text, image, created, updated
3. 모델 category - slub, name
'''
class Board(models.Model):
    # board안에 category, document가 속하는 형태도 가능
    pass
class Category(models.Model):
    # CharField 글자수 제한이 있음 -> DB에서 varchar 형태
    # text는 글자수 제한이 없음
    name = models.CharField(max_length=20)
    # DB에 보통 index 키값이 걸린다
    # unque값은 주의! 겹치지 않는다 -> board가 있다면 1게시판에 질문,답변 2게시판에 질문, 답변이 있다면 쓰면안됨
    # allow_unicode 한글을 사용한다면 사용
    slug = models.SlugField(max_length=30, db_index=True, unique=True, allow_unicode=True)
    # meta랑 같을 수도 있고 다를 수 있다
    description = models.CharField(max_length=200, blank=True)
    # 검색엔진에 제공해주기 위해
    meta_description = models.CharField(max_length=200, blank=True)

    class Meta:
        # DB에 기본적으로 설정될 정렬값
        ordering = ['slug']

# Setting에 있는 User 모델을 커스텀한 경우 불러서 써야하니까
from django.contrib.auth import get_user_model
class Document(models.Model):
    # 다른 쪽 참조하니까 ForeignKey -> on_delete
    # related_name 카테고리 입장에서 documents
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, db_index=True, unique=True, allow_unicode=True)
    text = models.TextField()
    # upload_to 동적으로 경로 설정 가능 ex) 유저별로 폴더를 할당 하는 경우
    image = models.ImageField(upload_to='board_images/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)