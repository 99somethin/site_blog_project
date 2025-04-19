from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import logout
from pyexpat.errors import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginForm, UpdateProfileForm, UpdateUserForm
# Create your views here.


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home_page')
    template_name = "accounts/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            return redirect(reverse('login'))
        return render(request, self.template_name, {'form': form})


class MyLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('home_page')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(MyLoginView, self).form_valid(form)

def MyLogoutView(request):
    logout(request)
    return redirect(reverse('home_page'))


class MyResetView(PasswordResetView):
    html_email_template_name = 'accounts/password_reset_email.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('reset_done')
    template_name = 'accounts/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MyResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Profile(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'acc_registration/profile.html',
                      {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST ,instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES,instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(reverse('users-profile'))



class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('users-profile')