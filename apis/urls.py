from django.urls import path
from . import views

urlpatterns = [
    path('register', views.user_registration),
    path('login',views.user_login),
    path('test',views.test_fun)
]
