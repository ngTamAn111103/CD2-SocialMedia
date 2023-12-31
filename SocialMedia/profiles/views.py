
from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout,get_user_model
from django.views.generic import CreateView,UpdateView,DetailView, ListView
from .models import Profile, Relationship,ProfileManager
from posts.models import Post,Comment,Image
from .form import ProfileModelForm, SignUpModelForm,LoginModelForm,ChangePasswordModelForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from posts.forms import PostModelForm,CommentModelForm,EditPostModelForm, EditCmtModelForm
from django.contrib.auth.models import User






# Create your views here.
@login_required
def my_profile_view(request):
    #print('================================================================')
    #print('================================================================')
    #print('================================================================')
    # post = get author == user đăng nhập
    profile = get_object_or_404(Profile, username=request.user)
    cover = profile.cover
    # Lấy danh sách bài viết của bản thân
    my_posts = Post.objects.filter(author=profile).all()
    
    
    # new comment form
    c_form = CommentModelForm(request.POST or None)
    # danh sách Relationship có liên quan đến mình + đã accepted
    friends = Relationship.objects.filter((Q(sender=profile) | Q(receiver=profile)), status='accepted')
    my_friends=[]
    for friend in friends:
        if friend.sender == profile:
            my_friends.append(friend.receiver)
        else:
            my_friends.append(friend.sender)
    # edit post
    post_edit_id = request.POST.get('post_edit_id')
    post_edit = Post.objects.filter(id=post_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_p_form = EditPostModelForm(request.POST or None, request.FILES or None, instance=post_edit)
    # edit cmt
    cmt_edit_id = request.POST.get('edit_cmt_id')
    cmt_edit = Comment.objects.filter(id=cmt_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_c_form = EditCmtModelForm(request.POST or None, instance=cmt_edit)
    # Chỉnh sửa chính chủ từ form, không qua phương thức GET
    if request.method == 'POST':
        # delete cmt
        cmt_del_id = request.POST.get('cmt_del_id')
        if cmt_del_id:
            #print("if post_del_id:")
            # Xóa bài viết
            Comment.objects.filter(id=cmt_del_id).delete()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # delete post 
        post_del_id = request.POST.get('post_del_id')
        if post_del_id:
            #print("if post_del_id:")
            # Xóa bài viết
            Post.objects.filter(id=post_del_id).delete()
            return redirect('/profiles/myprofile/')  # Chuyển hướng sau khi gửi thành công
        
        # edit post
        elif edit_p_form.is_valid() & (post_edit_id is not None):
            print("elif edit_p_form.is_valid():")
            post_edit = edit_p_form.save(commit=False)
            post_edit.author = profile
            post_edit.save()
            post_edit.images.all().delete()
            # Xử lý mỗi file tải lên riêng biệt
            for file in request.FILES.getlist('image'):
                Image.objects.create(post=post_edit, image=file)
            return redirect('/')  # Chuyển hướng sau khi gửi thành công

            return redirect('/profiles/myprofile/')  # Chuyển hướng sau khi gửi thành công
        # edit cmt
        elif (edit_c_form.is_valid()) & (cmt_edit_id is not None):
            #print('elif edit_c_form.is_valid():')
            instance = edit_c_form.save(commit=False)
            instance.user = profile
            instance.save()
            return redirect('/profiles/myprofile/')  # Chuyển hướng sau khi gửi thành công
        # Tạo cmt
        elif c_form.is_valid():
            #print(' elif c_form.is_valid():')
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm
            return redirect('/profiles/myprofile/')  # Chuyển hướng sau khi gửi thành công
        else:
            #print(edit_c_form.errors)
            pass
        
        
    context = {
        'profile': profile,
        'friend_list':my_friends,
        'my_posts':my_posts,
        'c_form':c_form,
        'edit_c_form':edit_c_form,
        'cover': cover,


    }
    #print('================================================================')
    #print('================================================================')
    #print('================================================================')
    return render(request, 'profiles/myprofile.html', context)
    
# Hàm này Tâm An code: Nhưng đừng kêu Tâm An giải thích....
class SignUp(CreateView):
    # Xử dụng form custom
    form_class = SignUpModelForm
    # Đường dẫn trả về nếu form submit thành công
    success_url = reverse_lazy('login')
    # Form sẽ chạy trên trang
    template_name = "account/register.html"
    
    
    # @transaction.atomic
    def form_valid(self, form):
        # Lấy dữ liệu từ form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        country = form.cleaned_data['country']
        gender = form.cleaned_data['gender']
        birthday = form.cleaned_data['birthday']
        email = form.cleaned_data['email']
        
        # Lấy tài khoản
        username = form.cleaned_data['username']
        # Kiểm tra và gán mật khẩu
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        
        # Đầu tiên, lấy đối tượng User
        User = get_user_model()
       
        # Tài khoản đã tồn tại
        if User.objects.filter(username=username).count() > 0:
            return HttpResponse("Tài khoản đã tồn tại")
        # Tài khoản chưa tồn tại
        else:
            if str(password1) != str(password2):
                # Tạo đối tượng User và gán mật khẩu
                user = User(username=username)
                # Đặt mật khẩu
                user.set_password(password1)  # Đảm bảo mật khẩu được mã hóa

                # Tạo đối tượng Profile và lưu vào cơ sở dữ liệu
                profile = Profile(email=email,username=user, first_name=first_name, last_name=last_name, country=country, gender=gender, birthday=birthday)
                
                user.save()
                profile.save()
                
                
                # return redirect(self.success_url,context )  # Chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
                return redirect(self.success_url)

            else:
                return HttpResponse("Mật khẩu xác thực không khớp!")


    
class Login(LoginView):
    template_name = 'account/login.html'
    form_class = LoginModelForm

    success_url = reverse_lazy('posts')  # Thay 'index' bằng tên view của trang index.html của bạn
    def form_valid(self, form):
        # Đăng nhập người dùng
        login(self.request, form.get_user())
        return super().form_valid(form)
    
# Lâm : xử lý đổi mk
#  1 kiểm tra: mk cũ đúng ko
# 2: 2 mk mới có == nhau ko 
#  3: nếu 2 mk mới == nhau: xử lý là ghi lại password cho username, co mã hóa
#  user.set_password(password1)  # Đảm bảo mật khẩu được mã hóa
# SignUp
# XỬ LÝ THUẬT TOÁN
# form_valid
# str(password1) != str(password2) CÓ THỂ HƠI NGƯỢC ĐỜI 1 TÍ

class UserProfileDetailView(DetailView):
    model = get_user_model()
    template_name = "account/user_profile.html"
    context_object_name = "user_profile"

class ChangePassword(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ChangePasswordModelForm
    template_name = "profiles/changepassword.html"
    success_url = reverse_lazy('logout')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        password_old = form.cleaned_data['password_old']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if user.check_password(password_old):
            if password1 != password2:
                user.set_password(password1)
                user.save()
                return super().form_valid(form)
            else:
                form.add_error(None, "Mật khẩu xác thực không khớp!")
        else:
            form.add_error(None, "Mật khẩu cũ không đúng.")

        return self.form_invalid(form)
    

# Trả về những lời mời kết bạn có receiver là user
def invites_received_view(request):
    profile = Profile.objects.get(username=request.user)
    qs = Relationship.objects.invatations_received(profile)
    # Chỉ lấy thằng sender trong relationship
    result = list(map(lambda x: x.sender,qs))
    is_empty = False
    if len(result) ==0:
        is_empty = True
    context = {
        'qs': result,
        'is_empty':is_empty,
    }
    return render(request, 'profiles/my_invites.html',context)

def accept_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk = pk)
        receiver = Profile.objects.get(username = request.user)
        rel = get_object_or_404(Relationship,sender=sender, receiver=receiver)
        if  rel.status == 'send':
            rel.status = 'accepted'
            rel.save()

    return redirect('profiles:my_invites_view')
def reject_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(username = request.user)
        sender = Profile.objects.get(pk = pk)
        rel = get_object_or_404(Relationship,sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my_invites_view')

# Tìm các profiles có sẵn để mời kết bạn,
def invite_profiles_list_view(request):
    user = request.user
    # Lấy tất cả danh sách hồ sơ <=> loại trừ mình
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {
        'qs': qs,
    }
    return render(request, 'profiles/to_invite_list.html',context)

def profiles_list_view(request):
    user = request.user
    # Lấy tất cả danh sách hồ sơ <=> loại trừ mình
    qs = Profile.objects.get_all_profiles(user)
    context = {
        'qs': qs,
    }
    return render(request, 'profiles/profile_list.html',context)

# Trang cá nhân của người khác:
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')

        profile = Profile.objects.get(slug=slug)
        return profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(username=user)
        context['profile'] = profile

        #  Mối quan hệ có người gửi là mình
        rel_r = Relationship.objects.filter(sender=profile)
        # Mối quan hệ có người nhận là mình
        rel_s = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []
        print(rel_r)
        print(rel_s)
        # lấy thằng profile.username bỏ vảo rel_receiver
        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        # lấy thằng profile.username bỏ vảo rel_sender
        for item in rel_s:
            rel_sender.append(item.sender.username)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] =rel_sender
        context['posts'] =self.get_object().get_all_authors_posts()
        context['len_posts'] =True if len(self.get_object().get_all_authors_posts()) > 0 else False

        
        
        return context



class ProfileListView(ListView):
    model = Profile
    template_name= 'profiles/profile_list.html'
    # context_object_name = 'qs'
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(username=user)
        context['profile'] = profile

        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)

        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        for item in rel_s:
            rel_sender.append(item.receiver.username)

        context['rel_receiver'] =rel_receiver
        context['rel_sender'] =rel_sender
        context['is_empty'] = False
        if len(self.get_queryset())==0:
            context['is_empty'] = True
        
        return context
       
def send_invation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(username = user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status="send")

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')

def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(username=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')



# Hàm change profile
def change_profile(request):
    profile = get_object_or_404(Profile, username=request.user)
    confirm = False
    # Hiển thị thông tin trong form của người dùng đang đăng nhạp
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST':
        # Form hợp lệ
        if form.is_valid():
            #print("if form.is_valid():")
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
        


    }
    #print('================================================================')
    #print('================================================================')
    #print('================================================================')
    return render(request, 'profiles/change_profile.html', context)


# Hàm xem toàn bộ danh sách bạn bè
class FriendsListView(ListView):
    model = Profile
    template_name = 'profiles/detail_all_friends.html'
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')

        profile = Profile.objects.get(slug=slug)
        # trả về profile của thằng detail
        return profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(username=user)
        context['profile'] = profile

        

       


        context['friends'] = self.get_object().get_friends()
        context['len_friends'] =True if len(self.get_object().get_friends()) > 0 else False

        
        
        return context


