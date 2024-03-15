"""
    Module name :- forms
"""

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    """
        Sign Up form.
    """
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
            __init__
        """
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    """
        Login Form
    """
    def __init__(self, *args, **kwargs):
        """
            __init__
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EditProfileForm(forms.ModelForm):
    """
        Edit Profile.
    """
    class Meta:
        """
            Meta class
        """
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }
