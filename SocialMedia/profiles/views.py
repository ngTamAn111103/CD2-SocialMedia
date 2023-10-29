
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout,get_user_model
from django.views.generic import CreateView
from .models import Profile
from .form import ProfileModelForm, SignUpModelForm,LoginModelForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required





# Create your views here.
@login_required
def my_profile_view(request):
    profile = Profile.objects.get(username = request.user)
    # Hiển thị thông tin trong form của người dùng đang đăng nhạp
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    
    # Chỉnh sửa chính chủ từ form, không qua phương thức GET
    if request.method == 'POST':
        # Form hợp lệ
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
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
                profile = Profile(username=user, first_name=first_name, last_name=last_name, country=country, gender=gender, birthday=birthday)
                
                user.save()
                profile.save()
                
                
                # return redirect(self.success_url,context )  # Chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
                return redirect(self.success_url)

            else:
                return HttpResponse("Mật khẩu xác thực không khớp!")


    
class Login(LoginView):
    template_name = 'account/login.html'
    form_class = LoginModelForm

    success_url = reverse_lazy('profiles:my_profile_view')  # Thay 'index' bằng tên view của trang index.html của bạn
    def form_valid(self, form):
        # Đăng nhập người dùng
        login(self.request, form.get_user())
        return super().form_valid(form)
    