from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Message, Profile
class MessageForm(forms.Form):
    recipient = forms.CharField(label='Recipient', max_length=150)
    subject = forms.CharField(label='Subject', max_length=255)
    body = forms.CharField(label='Message', widget=forms.Textarea)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    error_messages = {
        'password_requirements': _('Your password must consist of at least 8 characters and contain one capital letter and one digit.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_('Your password must consist of at least 8 characters and contain one capital letter and one digit.'),
    )
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError(self.error_messages['password_requirements'], code='password_requirements')

        if not any(char.isupper() for char in password1):
            raise forms.ValidationError(self.error_messages['password_requirements'], code='password_requirements')

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError(self.error_messages['password_requirements'], code='password_requirements')

        return password1
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')



class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
        model = Profile
        fields = ('picture',)
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].initial = self.instance.user.username
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=self.instance.user.username).exists():
            raise forms.ValidationError('Email is already in use.')
        return email
    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return super(EditProfileForm, self).save(commit=commit)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
class EditUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
        }
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)