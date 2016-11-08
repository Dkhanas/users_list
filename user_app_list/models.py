from __future__ import unicode_literals


from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class UserManger(BaseUserManager):
    def _create_user(self, phone, password, is_staff,
                     is_superuser, **extra_fields):
        now = timezone.now()
        user = self.model(phone=phone, is_superuser=is_superuser,
                          is_staff=is_staff, is_active=True,
                          create_date=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        return self._create_user(phone, password, False, False,
                                 **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        return self._create_user(phone, password, True, True,
                                 **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, default='',
                                  verbose_name=_("First name"), db_index=True
                                  )
    last_name = models.CharField(max_length=30, default='',
                                 verbose_name=_("Last name"),
                                 db_index=True
                                 )
    phone = models.IntegerField(default=None, verbose_name=_('Phone'),
                                db_index=True, unique=True,
                                )
    address = models.TextField(default='', verbose_name=_('Address'),
                               max_length=3000, db_index=True
                               )
    create_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                                                   'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
          help_text=_('Designates whether this user should be treated as '
          'active. Unselect this instead of deleting accounts.'))

    USERNAME_FIELD = 'phone'
    objects = UserManger()

    def __unicode__(self):
        if not self.first_name and not self.last_name:
            return "{}".format(self.phone)
        return "{} {}".format(self.first_name, self.last_name)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name


class Comments(models.Model):
    author = models.ForeignKey('User', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               related_name='author')
    text = models.TextField(default='', max_length=3000,
                            verbose_name=_('Comment text')
                            )
    raiting = models.IntegerField(default=None)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']

    def __unicode__(self):
        return self.text



