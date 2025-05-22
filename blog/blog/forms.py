from django import forms

class CustomerLoginForm(forms.Form):
    user_mail = forms.EmailField(label="Email")
    user_password = forms.CharField(label="Password", widget=forms.PasswordInput)