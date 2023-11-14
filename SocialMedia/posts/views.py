from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Like
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required 
from .forms import PostModelForm,CommentModelForm,EditPostModelForm, EditCmtModelForm
from django.http import JsonResponse
from profiles.models import Relationship
from django.views.generic import UpdateView,DeleteView
from django.db.models import Q
from .models import Comment

# Create your views here.
@login_required()
def post_comment_create_listview(request):
    # lấy tất cả bài viết
    # qs = Post.objects.all()
    
    
    

    # profile của thằng đăng đăng nhập
    profile = Profile.objects.get(username=request.user)
    
    # Bạn bè của profile
    friends = Relationship.objects.filter((Q(sender=profile) | Q(receiver=profile)), status='accepted')

    # List rõng
    posts = []

    # Lấy tất cả các bài viết của bạn bè và thêm vào danh sách
    for friend in friends:
        if friend.sender == profile:
            posts += Post.objects.filter(author=friend.receiver)
        else:
            posts += Post.objects.filter(author=friend.sender)

    # Lấy tất cả các bài viết của bạn và thêm vào danh sách
    your_posts = Post.objects.filter(author=profile)

    # Gộp danh sách bài viết của bạn bè và của bạn
    posts += list(your_posts)

    # Sắp xếp danh sách bài viết theo trường "created" (ngày tạo) giảm dần
    posts.sort(key=lambda post: post.created, reverse=True)


    # new post form
    p_form = PostModelForm(request.POST or None, request.FILES or None)
    # new comment form
    c_form = CommentModelForm(request.POST or None)

    # edit post
    post_edit_id = request.POST.get('post_edit_id')
    post_edit = Post.objects.filter(id=post_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_p_form = EditPostModelForm(request.POST or None, request.FILES or None, instance=post_edit)

    # edit cmt
    cmt_edit_id = request.POST.get('edit_cmt_id')
    cmt_edit = Comment.objects.filter(id=cmt_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_c_form = EditCmtModelForm(request.POST or None, instance=cmt_edit)

    # Lấy danh sách lời mời kết bạn gửi đến mình
    friend_requests = Relationship.objects.filter((~Q(sender=profile)| ~Q(receiver= profile)), status='send')
    
    # Accept request friends
    print("--------------------------------")
    
    
    # Xử lý 
    if request.method == "POST":
        print('if request.method == "POST":')

        

        # delete post 
        post_del_id = request.POST.get('post_del_id')
        if post_del_id:
            print("if post_del_id:")
            # Xóa bài viết
            Post.objects.filter(id=post_del_id).delete()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # delete cmt
        cmt_del_id = request.POST.get('cmt_del_id')
        if cmt_del_id:
            print("if post_del_id:")
            # Xóa bài viết
            Comment.objects.filter(id=cmt_del_id).delete()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # edit post
        elif edit_p_form.is_valid() & (post_edit_id is not None):
            print("elif edit_p_form.is_valid():")
            instance = edit_p_form.save(commit=False)
            instance.author = profile
            instance.save()

            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # edit cmt
        elif (edit_c_form.is_valid()) & (cmt_edit_id is not None):
            print('elif edit_c_form.is_valid():')

            instance = edit_c_form.save(commit=False)
            instance.user = profile
            instance.save()

            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # Tạo post
        elif p_form.is_valid():
            print("elif p_form.is_valid():")
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # Tạo cmt
        elif c_form.is_valid():
            print('elif c_form.is_valid():')
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
            return redirect('/')
        # Tính năng kết bạn
        elif 'relationship_id' in request.POST and 'btn_relationship' in request.POST:
            print("accept_delete_request(request)")
            accept_delete_request(request) 

        else:
            # pass
            print("không có cái nào vào cả")
            
        
        
    # Mảng trả về
    context = {
        'qs': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'edit_p_form': edit_p_form,
        'friend_requests': friend_requests,


    }
    print("--------------------------------")
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

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }


    return redirect('/')
    # return HttpResponse("Like thành công")

def accept_delete_request(request):

    relationship_id=request.POST.get('relationship_id')
    relationship = Relationship.objects.get(id=relationship_id)
        # button
    if request.POST.get('btn_relationship') =='Accept':
        relationship.status = 'accepted'
        relationship.save()
    elif request.POST.get('btn_relationship') =='Delete':
        relationship.delete()





    


    
