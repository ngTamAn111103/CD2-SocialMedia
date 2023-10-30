from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

# Tín hiệu: Khi người dùng tạo tài khoản mật khẩu (User) -> Đồng thời tự động tạo Profile
# @receiver(post_save, sender=User)
# def post_save_create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(username=instance)


# Tín hiệu: Khi gửi kết bạn và đồng ý: 2 người sẽ có trong danh sách bạn bè của đối phương
@receiver(post_save, sender=Relationship)
def post_save_add_to_friend(sender, instance, created, **kwargs):
    print(123)
    sender_= instance.sender
    receiver_= instance.receiver
    
    if instance.status == "accepted":
        sender_.friends.add(receiver_.username) 
        receiver_.friends.add(sender_.username)
        sender_.save()
        receiver_.save()