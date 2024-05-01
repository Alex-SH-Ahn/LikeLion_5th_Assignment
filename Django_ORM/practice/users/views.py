from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth

User = get_user_model()

#회원가입
def signup(request):
  if request.method == 'POST':
    if request.POST['password1'] == request.POST['password2']:
      user = User.objects.create_user(
        username = request.POST['username'],
        password = request.POST['password1'],
        email = request.POST['email'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
      )
      #User는 장고에서 기본 제공하는 객체라 따로 save하지 않아도 됨

      profile = Profile(
        user=user,
        nickname=request.POST['nickname'],
        image=request.FILES.get('profile_image'),
      )

      #프로필은 내가 만든거라 데이터베이스에 따로 저장
      profile.save()
      auth.login(request, user)

      return redirect('home') #회원가입 성공하면 홈페이지로 돌아가기
    return render(request, 'signup.html') #회원가입 실패시 다시 회원가입 페이지로 이동
  return render(request, 'signup.html')

# 로그인
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password) 
    #기존 정보와 새로 들어온 정보가 일치하는지 장고에서 확인해줌

    if user is not None:
      auth.login(request, user)
      return redirect('home') # 정보가 일치하고 로그인 정보가 None이 아니라면 홈페이지로
    return render(request, 'login.html') # 로그인 정보가 None이면 그대로
  return render(request, 'login.html') # POST가 아닌 경우에도 그대로

# 로그아웃
def logout(request):
  auth.logout(request)
  return redirect('home')

def profile(request, user_id):
  user = get_object_or_404(User, id=user_id)
  return render(request, 'profile.html', {'user': user})
