from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


def user_avatar_directory_path(instance, filename):
    return 'user/{0}/avatar/{1}'.format(str(instance.email)[0:str(instance.email).index('@')], filename)


def user_identifier_image_directory_path(instance, filename):
    return 'user/{0}/identifier-image/{1}'.format(str(instance.user.email)[0:str(instance.user.email).index('@')],
                                                  filename)


class UserManager(BaseUserManager):

    def create_user_identity(self, user):
        identity = Identity(user=user)
        identity.save()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        self.create_user_identity(user)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(_('avatar'), upload_to=user_avatar_directory_path, blank=True, null=True)
    code = models.IntegerField(_('code'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'کاربران'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.first_name + " " + self.last_name if self.first_name else self.email[0:self.email.index('@')]


REQUESTED = '1'
IDENTIFIED = '2'
UNIDENTIFIED = '3'
STATUS_CHOICES = (
    (IDENTIFIED, 'احراز شده'),
    (REQUESTED, 'درخواست احراز'),
    (UNIDENTIFIED, 'احراز نشده')
)


class Identity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    identifier_image = models.ImageField(upload_to=user_identifier_image_directory_path, blank=True, null=True,
                                         verbose_name='عکس احراز هویت')
    request_time = models.DateTimeField(null=True, blank=True, verbose_name='زمان درخواست')
    expire_time = models.DateTimeField(blank=True, null=True, verbose_name='زمان ابطال')
    status = models.CharField(choices=STATUS_CHOICES, default=UNIDENTIFIED, verbose_name='وضعیت', max_length=1)

    def __str__(self):
        return str(self.user) + ' ' + self.status

    class Meta:
        ordering = ['-request_time']
        verbose_name = 'احراز هویت'
        verbose_name_plural = 'احراز هویت'
