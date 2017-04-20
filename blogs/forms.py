from django import forms
from .models import Post ,Comment ,File

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)