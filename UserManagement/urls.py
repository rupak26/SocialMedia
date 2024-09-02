from django.urls import path
from .views import userLogoutView,ForgetPassword,UserRegistrationView,VerifyRegistrationView,userLoginView,userPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name = 'Registration'),
    path('verify/',VerifyRegistrationView.as_view(),name='Verification'),
    path('login/',userLoginView.as_view(),name='login'),
    path('forget_pass/',ForgetPassword.as_view(),name='ForgetPassword'),
    path('reset_pass/',userPasswordResetView.as_view(),name='Reset_Password'),
    path('logout/',userLogoutView.as_view(),name='logout'),
]