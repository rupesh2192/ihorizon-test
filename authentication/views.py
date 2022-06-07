from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from . import forms
from .models import UserTypeChoices


class RegisterView(FormView):
    template_name = "auth/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.user_type == UserTypeChoices.CUSTOMER.value:
            return reverse_lazy("supportdesk_customer_requests")
        return reverse_lazy("supportdesk_agent_requests")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
