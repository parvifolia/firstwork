from django import forms
from .models import Post,Comment
from captcha.fields import ReCaptchaField


class PostForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = ('title', 'text',)