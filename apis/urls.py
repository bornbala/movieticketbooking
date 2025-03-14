from django.urls import path
from . import views

urlpatterns = [
    path('user_register', views.user_registration),
    path('user_login',views.user_login),
    path('test_user',views.test_fun)
]
