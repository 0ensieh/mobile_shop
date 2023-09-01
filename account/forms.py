from django import forms
from .models import User
from order.models import Address
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'ssn')
        


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, label='ایمیل')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text with-border'}), label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text with-border'}), label='تکرار رمز عبور')
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-input'}), 
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-input'})
        }

        labels = {
                'password1': 'رمز عبور', 
                'password2': 'تکرار رمز عبور',
                'email': 'ایمیل'
            }



class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email',
         'is_active', 'ssn', 'wallet_amount', 'is_admin', 'is_superuser', 'password')


