from django import forms

from account.models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text','qr')