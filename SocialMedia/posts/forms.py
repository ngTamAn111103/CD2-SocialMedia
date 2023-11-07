from django import forms
from .models import Post, Comment
# Tạo 1 bài viết mới
class PostModelForm(forms.ModelForm):
    # Sửa css ở đây Thành ơi
    
    
    
    
    
    class Meta:
        model = Post
        fields = ('content', 'image')
        
        
        
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='Bình luận', 
                           widget=forms.TextInput(attrs={'placeholder':'Bình luận bài viết'}))
    # Sửa css ở đây Thành ơi
    
    
    
    
    
    class Meta:
        model = Comment
        fields = ('body',)