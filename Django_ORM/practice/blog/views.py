from django.contrib.auth.decorators import login_required #! 추가된 코드
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag
from .forms import BlogForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

User = get_user_model()

def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    tags = blog.tag.all()
    return render(request,'detail.html',{'blog':blog, 'comments':comments, 'tags':tags})

def new(request):
    tags = Tag.objects.all()
    return render(request,'new.html', {'tags':tags})

# def create(request):
#     new_blog = Blog()
#     new_blog.title = request.POST.get('title')
#     new_blog.content = request.POST.get('content')
#     new_blog.image = request.FILES.get('image')
#     new_blog.author = request.user
#     new_blog.save()
#     tags = request.POST.getlist('tags')
#     for tag_id in tags:
#         tag = Tag.objects.get(id=tag_id)
#         new_blog.tag.add(tag)

#     return redirect('detail', new_blog.id)

@login_required
def create(request):
    if request.method == 'POST':
        new_blog = Blog()
        new_blog.title = request.POST.get('title')
        new_blog.content = request.POST.get('content')
        if 'image' in request.FILES:
            new_blog.image = request.FILES.get('image')
        new_blog.author = request.user
        new_blog.save()
        tags = request.POST.getlist('tags')
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            new_blog.tag.add(tag)
        return redirect('blog:detail', new_blog.id)
    else:
        tags = Tag.objects.all()
        return render(request, 'new.html', {'tags': tags})

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id)
    if edit_blog.author != request.user:
        return redirect('blog:home')
    return render(request, 'edit.html', {'edit_blog':edit_blog})

def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('blog:detail', old_blog.id)

    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)

    return render(request, 'new.html', {'old_blog':old_blog})

def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('blog:home')

def create_comments(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    # blog가 없으면 댓글도 있으면 안되니까 get object or 404
    comment.author = request.user
    comment.save()

    return redirect('blog:detail', blog_id)

def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog':blog})

#! 좋아요 기능 함수
@require_POST
def likes(request, blog_pk):
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, pk=blog_pk)
        if request.user in blog.like_users.all():
            blog.like_users.remove(request.user)
        else:
            blog.like_users.add(request.user)
        return redirect('blog:detail', blog_pk) #* 좋아요 추가/삭제 후 상세 페이지로
    return redirect('login') #* 로그인 되지 않았으면 로그인 페이지로
