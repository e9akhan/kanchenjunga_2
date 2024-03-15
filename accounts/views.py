"""
    Module name :- views.
"""


from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.forms import SignUpForm, LoginForm, EditProfileForm
from accounts.models import CustomUser

# Create your views here.
class SignUp(CreateView):
    """
        Sign up class.
    """
    model = get_user_model()
    form_class = SignUpForm
    template_name = 'accounts/form.html'
    success_url = 'accounts:login'


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        context['header'] = 'Sign Up'
        return context


class Login(LoginView):
    """
        Login
    """
    form_class = LoginForm
    template_name = 'accounts/form.html'
    next_page = 'store:dashboard'

    # def post(self, request, *args, **kwargs):

    #     if not request.user.is_superuser:
    #         custom_user = CustomUser.objects.filter(user=request.user.id).reverse()[0]
    #         if custom_user.rejected:
    #             messages.info(request, 'Your approval has been rejected. Please contact the administrator.')
    #             return redirect('accounts:login')

    #         if not custom_user.approved:
    #             messages.info(request, 'You have not been approved.')
    #             return redirect('accounts:login')
        
    #     return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['header'] = 'Login'
        return context


class Logout(LogoutView):
    """
        Logout
    """
    next_page = 'accounts:login'


class EditProfile(UpdateView):
    """
        Edit Profile.
    """
    model = get_user_model()
    template_name = 'accounts/form2.html'
    success_url = 'store:dashboard'
    form_class = EditProfileForm


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile'
        context['header'] = 'Edit Profile'
        return context


class DeleteProfile(DeleteView):
    """
        Delete Profile
    """
    model = get_user_model()
    template_name = 'accounts/form2.html'
    success_url = 'accounts:login'


    def get_context_data(self, **kwargs):
        """
            get_context_data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Profile'
        context['header'] = 'Delete Profile'
        context['headline'] = f'Do you really want to delete {self.get_object()}'
        return context
