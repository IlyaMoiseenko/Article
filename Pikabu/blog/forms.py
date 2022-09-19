from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from blog.models import Article, Comment


class ArticleAddForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text')


class SignInForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
