from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login after successful signup
    template_name = 'authentication/signup.html'

class DevLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'authentication/login.html'
    next_page = reverse_lazy('home') # Redirect to home page after successful login

class DevLogoutView(LogoutView):
    next_page = reverse_lazy('login') # Redirect to login page after logout

class DevPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done') # Redirect to a success page
    template_name = 'authentication/password_change.html'