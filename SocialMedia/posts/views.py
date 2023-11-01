from django.shortcuts import render,redirect
from .models import Post,Like
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse_lazy

# Create your views here.
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
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }

        # return JsonResponse(data, safe=False)
    return redirect(reverse_lazy('main_post_view'))
    return HttpResponse("Like thành công")