from django.shortcuts import render
from .models import Post
from django.http import HttpResponse
# Create your views here.
def post_comment_create_listview(request):
    qs = Post.objects.all()
    
    context = {
        'qs': qs,
    }

    return render(request, 'main.html', context)