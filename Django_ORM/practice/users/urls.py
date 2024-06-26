from django.urls import path
from .views import *

urlpatterns = [
  path('signup/', signup, name='signup'),
  path('login/', login, name='login'),
  path('logout/', logout, name='logout'),
  path('profile/<int:user_id>', profile, name='profile'),
]
