from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    code = forms.CharField()


class UploadForm(forms.Form):
    pass
