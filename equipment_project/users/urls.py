from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.urls import (
    path,
)

from . import (
    views,
)

app_name = 'users'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(
             template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(
             template_name='users/login.html'),
         name='login'),
    path('password_reset_done/',
         views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/',
         views.PasswordReset.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),

]
