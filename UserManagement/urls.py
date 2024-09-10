from django.urls import path
from .views import UserLogoutView,ForgetPassword,UserRegistrationView,VerifyRegistrationView,UserLoginView,UserPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name = 'Registration'),
    path('verify/',VerifyRegistrationView.as_view(),name='Verification'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('forget-password/',ForgetPassword.as_view(),name='Forget_Password'),
    path('reset-password/',UserPasswordResetView.as_view(),name='Reset_Password'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
]