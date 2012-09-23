from django import forms
import models


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)


class PostForm(forms.Form):
    title = forms.CharField(max_length=120)
    body = forms.CharField(max_length=models.Post._meta.get_field('body').max_length, widget=forms.Textarea)
    markup = forms.BooleanField(required=False, label = "Check if you are posting ASCII Art (otherwise interpret post like reddit does)")
    quality = forms.BooleanField(required=False, label = "Check if good post. (if no it will go in the free speech bin... err space)")


class AnonPostForm(forms.Form):
    title = forms.CharField(max_length=120)
    body = forms.CharField(max_length=models.Post._meta.get_field('body').max_length, widget=forms.Textarea)
    markup = forms.BooleanField(required=False, label = "Check if you are posting ASCII Art (otherwise interpret post like reddit does)")


class VoteForm(forms.Form):
    pass

