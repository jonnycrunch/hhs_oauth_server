from django import forms

from django.utils.translation import ugettext_lazy as _


class MFACodeForm(forms.Form):
    code = forms.CharField(widget=forms.PasswordInput, max_length=30,
                           label=_('Code*'))
    required_css_class = 'required'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, max_length=150,
                               label=_('Password'))
    required_css_class = 'required'

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.strip().lower()
