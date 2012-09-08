from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)


class PostForm(forms.Form):
    title = forms.CharField(max_length=120)
    body = forms.CharField(max_length=2000, widget=forms.Textarea)


