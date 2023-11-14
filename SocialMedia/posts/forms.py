from django import forms
from .models import Post, Comment
from django.db import models
# Tạo 1 bài viết mới
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image','visibility')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'content-post','placeholder':'Bạn đang nghĩ gì?'}),
            'image': forms.FileInput(attrs={'class': 'image-post'}),
            'visibility': forms.Select(attrs={'class': 'visibility'}),
        }

        
        
        
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='Bình luận', 
                           widget=forms.TextInput(attrs={'placeholder':'Bình luận bài viết'}))        
    class Meta:
        model = Comment
        fields = ('body',)

class EditPostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content','image', 'visibility',)
class EditCmtModelForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('body',)