from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUserManager(UserManager):
    pass


class UserRoles(models.TextChoices):
    USER = 'User'
    MODERATOR = 'Moderator'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.USER)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user',
    )

    objects = CustomUserManager()

class Moderator(CustomUser):

    class Meta:
        proxy = True

    def has_module_perms(self, app_label):
        return False

    def has_perm(self, perm, obj=None):
        if perm == 'app.add_model':
            return False
        return True

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, default='', blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, created, **kwargs):

    print(instance)

    user = instance

    if created:
        profile = Profile(user=user)
        profile.save()
