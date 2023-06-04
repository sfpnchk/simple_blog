from ckeditor.widgets import CKEditorWidget
from django import forms

from posts.models import Posts, Comment


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Posts
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
