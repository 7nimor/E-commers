from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('verify/',views.UserVerifyCodeView.as_view(),name='user_verify'),
    path('logout/',views.UserLogOutView.as_view(),name='user_logout'),
    path('login/',views.UserLoginView.as_view(),name='user_login'),
]