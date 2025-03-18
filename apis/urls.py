from django.urls import path
from . import views

urlpatterns = [
    path('email_verification',views.user_registration_email_verification),
    path('verify_email_otp',views.verify_email_otp),
    path('register', views.user_registration),
    path('login',views.user_login),
    path('test_user',views.test_fun)
]
