from django import forms 
from .models import Post,Comment

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postname', 'content' , 'banner' ]


class ModifyPostForm(forms.Form):
    postname = forms.CharField(max_length = 50 )
    content = forms.CharField(widget=forms.Textarea())
    banner = forms.ImageField(required = False)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

class ChangeProfilePhotoForm(forms.Form):
    new_photo = forms.ImageField(required=False, label="newpfp")

class CommentFormModel(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    
