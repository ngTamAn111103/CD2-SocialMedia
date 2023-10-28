# pass user http://127.0.0.1:8000/admin/auth/user/add/
from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Chưa có tiểu sử...", max_length=100)
    CHOICE_COUNTRY = (
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Hà Nội', 'Hà Nội'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hồ Chí Minh', 'Hồ Chí Minh'),
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
    country = models.CharField(max_length=50, blank=True, choices=CHOICE_COUNTRY)
    avatar = models.ImageField(default='avatar_default.jpg', upload_to='avatars/')
    cover = models.ImageField(blank=True, upload_to='covers/')
    friends = models.ManyToManyField(User, blank=True,related_name='friens')
    slug = models.SlugField(blank=True,)
    CHOICE_GENDER = (
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác'),
)
    gender = models.CharField(choices=CHOICE_GENDER, max_length=6, default='other')
    birthday = models.DateField(blank=True,default='2000-01-01')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    # Lấy danh sách bạn bè
    def get_friends(self):
        return self.friends.all()
    
    # Lấy số lượng bạn bè
    def get_count_friends(self):
        return (self.friends.all()).count()
    
    # Trả về trong admin thông tin 
    def __str__(self) -> str:
        return f'{self.username} / {self.created.strftime("%d-%m-%Y")}'
    
    # Hàm lưu
    def save(self, *args, **kwargs):
        # Slug cho profile
        self.slug_default()
        
        # Update hình ảnh default
        self.update_avatar_default()
        super().save(*args, **kwargs)
        
    # Hàm tạo slug cho profile
    def slug_default(self):
        ex = False
        # Nếu có họ và tên
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name)+" "+ str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug +" "+ str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        # Nếu không có họ và tên
        else:
            to_slug = str(self.username)
        self.slug = to_slug
        
    # Khi người dùng thay đổi giới tính && avatar đang ở mặc định
    # Avatar sẽ thay đổi theo
    def update_avatar_default(self):
        if self.gender == 'female' and self.avatar.name == 'avatar_default.jpg':
            self.avatar = 'avatar_default_nu.jpg'
            self.save()

        if self.gender == 'male' and self.avatar.name == 'avatar_default_nu.jpg':
            self.avatar = 'avatar_default.jpg'
            self.save()


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    STATUS_CHOICES = (
        ('send', "Gửi"),
        ('accepted', "Chấp nhận"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver} - {self.status}"