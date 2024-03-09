from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

from user.models import CustomUser
from ad.models import Ad


class Comment(models.Model):
    comment_text = models.TextField(max_length=1000, default='', blank=False)
    mark = models.IntegerField(default=5)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class CommentImages(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='comment/images')



@receiver(post_delete, sender = CommentImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)