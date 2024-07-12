import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.templatetags.static import static

PHONE_REGEX = RegexValidator(
    regex=r"^\+998([0-9][0-9]|99)\d{7}$",
    message="Please provide a valid phone number",
)


class UserManager(BaseUserManager):
    def create_user(self, username,  password=None, **extra_fields):

        if not username:
            raise ValueError('User must have a username')


        user = self.model(

            username=username,

            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        return self.create_user(username, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(unique=True, max_length=20)
    last_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=250, blank=True, null=True)
    old = models.IntegerField(default=0)
    SEX_CHOICES = [
        ('man', _('Man')),
        ('woman', _('Woman')),
    ]
    sex = models.CharField(max_length=5, choices=SEX_CHOICES)
    bio = models.CharField(max_length=1000, default=False,blank=True, null=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=21, unique=True, default="+998931112233", blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    join_date = models.DateTimeField(default=timezone.now)
    follow = models.ManyToManyField('self', symmetrical=False, related_name='user_follow', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_followers', blank=True)
    avatar = models.ImageField(upload_to='accounts/avatars/', default="defaultavatar/avatar.jpg")
    avatar_thumbnail = models.ImageField(upload_to='avatar/thumbnails/', blank=True, null=True)
    back_image = models.ImageField(upload_to='back_images/', blank=True, null=True)
    posts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name']

    def __str__(self):
        return f'{self.username} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_admin

    # @property
    # def avatar_url(self):
    #     if self.avatar:
    #         return self.avatar.url
    #     return static('defaultavatar/avatar.jpg')




