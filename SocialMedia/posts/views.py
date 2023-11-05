from django.shortcuts import render,redirect
from .models import Post,Like
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def post_comment_create_listview(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(username=request.user)
    context = {
        'qs': qs,
        'profile': profile,
    }

    return render(request, 'main.html', context)

def like_unlike_post(request):
    # Lấy user đăng nhập
    user = request.user
    
    if request.method == 'POST':
        # Lấy trường hidden post_id
        post_id = request.POST.get('post_id')
        # tìm bài đăng theo di
        post_obj = Post.objects.get(id=post_id)
        # lấy đối tượng user
        profile = Profile.objects.get(username=user)

        # user nằm trong danh sách đối tượng đã thích
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        
        # Cập nhật lại giá trị value
        # Nếu không có trường 'created'> đã tạo> Đã có dữ liệu trong db
        if not created:
            if like.value =='Like':
                like.value ='Unlike'
            else:
                like.value='Like'
        # Chưa like lần nào: chưa có dữ liệu database
        else:
            like.value='Like'
            
        post_obj.save()
        like.save()

        

    return redirect('/posts/')
    # return HttpResponse("Like thành công")