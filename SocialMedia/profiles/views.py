
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import View, TemplateView, ListView,DetailView, CreateView
from .models import Profile
from .form import ProfileModelForm, UserModelForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
# Create your views here.
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
    form_class = UserModelForm
    # Đường dẫn trả về nếu form submit thành công
    success_url = reverse_lazy('profiles:my_profile_view')
    # Form sẽ chạy trên trang
    template_name = "account/register.html"
    def form_valid(self, form):
        # Lấy dữ liệu từ form
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        country = form.cleaned_data['country']
        gender = form.cleaned_data['gender']
        birthday = form.cleaned_data['birthday']

        # Lấy đối tượng User đã tạo sau khi submit form
        user = form.save()

        # Tạo đối tượng Profile và lưu vào cơ sở dữ liệu
        profile = Profile(username=user, first_name=first_name, last_name=last_name, country=country, gender=gender, birthday=birthday)
        profile.save()

        return super().form_valid(form)

    