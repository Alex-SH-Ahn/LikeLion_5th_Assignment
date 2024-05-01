from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='blogs') #! 좋아요 기능 추가
    tag = models.ManyToManyField(to='Tag', blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_blogs', blank=True)
    #작성자와 블로그는 1:N 관계 (작성자1명 게시글 여러개)

    class Meta:
        db_table = 'blog'
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]

# 댓글
class Comment(models.Model):
    content = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, related_name='comments')
    # 1:N관계 - 하나의 글에 여러개의 댓글 달릴 수 있음
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='comments')
    # 1:N관계 - 한 명의 작성자가 여러개의 댓글 작성할 수 있음

    class Meta:
        db_table = 'comment'
    
    def __str__(self):
        return self.content + " | " + str(self.author)

# 태그
class Tag(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'tag'
    
    def __str__(self):
        return self.name