from django.urls import path, include
from . import views #.은 현재폴더의 디렉토리라는뜻. 즉 현재폴더의 views.py를 import하는것임

urlpatterns = [
path('', views.index, name='index'),
path('index_login', views.index_login, name='index_login'),
path('info.html', views.info, name='info'),
path('boderView.html', views.boderView, name='boderView'),
path('Login.html', views.Login, name='Login'),
path('join.html', views.join, name='join'),
path('Starting.html', views.Starting, name='Starting'),
path('info_login.html', views.info_login, name='info_login'),
path('boderView_login.html', views.boderView_login, name='boderView_login'),
path('boderRead.html', views.boderRead, name='boderRead'), # 'boderRead/<int:idx>/' -> name/<변수타입 : 넘겨줄변수>/
path('boderWrite.html', views.boderWrite, name='boderWrite'),
path('MyPage.html', views.MyPage, name='MyPage'),
path('CheckIdPw', views.CheckIdPw, name='CheckIdPw'),
path('Write', views.Write, name='Write'),
]

# path('Write_Comment1', views.Write_Comment1, name='Write_Comment1'),