from django.db import models
# Xử lý đuôi hình ảnh
from django.core.validators import FileExtensionValidator
# Xử lý user like bài
from profiles.models import Profile

# Create your models here.
class Post (models.Model):
    content = models.TextField(blank=False,default='')
    image = models.FileField(upload_to='post', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'mp4','mov'])], blank= True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    commented = models.ManyToManyField(Profile, blank=True, related_name='comments')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='posts')
    
    def __str__(self) -> str:
        return str(self.content[:50])
    
    def num_likes(self):
        return self.liked.all()
    
    def num_comments(self):
        return self.commented.all()
    
    class Meta:
        ordering = ('-created',)
        
class Comment (models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.pk)
    
LIKE_CHOICES = (
    # Chưa nhấn -> hiển thị thích
    ("Like", "Like"),
    # Đã nhấn -> chuyển sang ko thích nữa
    ("Unlike", "Unlike"),
)
class Like (models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}-{self.post}-{self.value}"