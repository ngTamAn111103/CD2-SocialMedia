from django import forms
from .models import Profile, User


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','bio','country','avatar','cover','gender','birthday')
        

class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(label='Họ')
    last_name = forms.CharField(label='Tên')
    username = forms.CharField(label='Tài khoản')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    # Chọn thành phố 
    CHOICE_COUNTRY = (
        ('Hồ Chí Minh', 'Hồ Chí Minh'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Hà Nội', 'Hà Nội'),
    ('Hải Phòng', 'Hải Phòng'),
    
    ('An Giang', 'An Giang'),
    ('Bà Rịa-Vũng Tàu', 'Bà Rịa-Vũng Tàu'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    )

    country = forms.ChoiceField(choices= CHOICE_COUNTRY, label="Thành phố")
    
    CHOICE_GENDER = (
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác'),
)
    gender = forms.ChoiceField(choices= CHOICE_GENDER, label="Giới tính")
    # birthday = forms.CharField(max_length=10, label="Ngày sinh",widget=forms.TextInput(placeholder="DD/MM/YYYY"))
    birthday = forms.CharField(max_length=10, label="Ngày sinh", 
                               widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
   



    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password1', 'password2', 'country','gender','birthday')
        