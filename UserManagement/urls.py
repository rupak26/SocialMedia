from django.urls import path
from .views import userLogoutView,ForgetPassword,UserRegistrationView,VerifyRegistrationView,userLoginView,userPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name = 'Registration'),
    path('verify/',VerifyRegistrationView.as_view(),name='Verification'),
    path('login/',userLoginView.as_view(),name='login'),
    path('forget-password/',ForgetPassword.as_view(),name='Forget_Password'),
    path('reset-password/',userPasswordResetView.as_view(),name='Reset_Password'),
    path('logout/',userLogoutView.as_view(),name='logout'),
]