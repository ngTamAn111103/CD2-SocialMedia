from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Like, Comment
from profiles.models import Profile, Relationship
from .models import Notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        
        Notification.objects.create(
            to_user=instance.post.author.username,
            notification_type=Notification.LIKE,
            # Thêm các trường khác nếu cần
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance.post.author.username,
            notification_type=Notification.COMMENT,
            # Thêm các trường khác nếu cần
        )

@receiver(post_save, sender=Relationship)
def create_relationship_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance.receiver.username,
            notification_type=Notification.ADDFRIEND,
            # Thêm các trường khác nếu cần
        )
