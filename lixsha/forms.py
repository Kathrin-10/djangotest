from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'Email'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'autocomplete': 'name', 'placeholder': 'Name'})
    )
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={'autocomplete': 'gender', 'placeholder': 'Gender'})
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'autocomplete': 'bday', 'placeholder': 'Date of Birth'})
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'dob', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')

        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Username is required')
        if not password:
            self.add_error('password', 'Password is required')

        return cleaned_data
