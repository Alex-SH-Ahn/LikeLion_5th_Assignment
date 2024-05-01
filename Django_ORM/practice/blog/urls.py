from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:blog_id>/', views.detail, name='detail'),
    path('blog/new/', views.new, name='new'),
    path('blog/create/', views.create, name='create'),
    path('blog/edit/<int:blog_id>/', views.edit, name='edit'),
    path('blog/update/<int:blog_id>/', views.update, name='update'),
    path('blog/delete/<int:blog_id>/', views.delete, name='delete'),
    path('blog/create_comment/<int:blog_id>/', views.create_comments, name='create_comment'),
    path('blog/new_comment/<int:blog_id>/', views.new_comment, name='new_comment'),
    path('like/<int:blog_pk>/', views.likes, name='like') #! 좋아요 추가/삭제 때 사용
]