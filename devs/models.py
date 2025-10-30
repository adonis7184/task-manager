from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


class Tech(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True
    )
    description = models.TextField(_('description'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tech')
        verbose_name_plural = _('teches')

class Team(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True
    )

    teches = models.ManyToManyField(Tech, related_name='teams')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))

    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        NON_BINARY = 'NB', 'Non-Binary'
        PREFER_NOT_TO_SAY = 'P', 'Prefer not to say'

    SOCIAL_CHOICES = [
        ('twitter', 'Twitter'),
        ('telegram', 'Telegram'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram')
    ]

    name = models.CharField(_('name'), max_length=255)
    gender = models.CharField(
        _('gender'),
        max_length=2,
        choices=GenderChoices.choices,
        blank=True,
        default=GenderChoices.PREFER_NOT_TO_SAY
    )
    birthday = models.DateField(_('birthday'))
    avatar = models.ImageField(upload_to='avatars/', verbose_name=_('avatar'), null=True, blank=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True)
    social_medias = MultiSelectField(choices=SOCIAL_CHOICES)

    # social = models.
    date_registered = models.DateTimeField(_('date registered'), default=timezone.now)
    leader = models.ForeignKey(
        'self', 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='team_members'
    )
    team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, 
        verbose_name=_('team'), 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.name == 'admin':
            raise ValidationError(_("You cannot set admin as developer's name"))

    class Meta:
        verbose_name = _("developer")
        verbose_name_plural = _("developers")
