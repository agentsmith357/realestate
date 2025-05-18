from django.urls import include, path
from . import views

urlpatterns = [
path('login',views.login),
path('auction/login',views.login),
path('/auction/login',views.login),
path('login_attempt',views.login_attempt,name="login_attempt"),
path('/',views.index,name="default_page"),
path('',views.index,name="default_page"),
path('view_page/',views.load_data,name="view_page"),
path('filter_data/',views.filter_data,name="filter_data"),
path('follow/',views.follow,name="follow"),
path('unfollow/',views.unfollow,name="unfollow"),
]