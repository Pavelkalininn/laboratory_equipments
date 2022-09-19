from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('web:index')
    template_name = 'users/signup.html'


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset.html'


class PasswordResetDoneView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('web:index')
    template_name = 'users/password_reset_done.html'
