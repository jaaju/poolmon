from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from decimal import Decimal
from enum import IntEnum


class PoolOwner(models.Model):
    USERNAME_FIELD = 'username'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)


class Pool(models.Model):
    user = models.ForeignKey(PoolOwner)
    name = models.CharField(
        max_length=50,
        help_text='Give a name for the pool.',
        unique=True,
        null=False)
    depth = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='Max. depth (ft.)')
    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Surface area (sq. ft.)')
    size = models.IntegerField(help_text='Pool volume (gallons)')
    fill_rate = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(99)],
        help_text='# times/week the pool is filled.')
    covered = models.BooleanField(help_text='Is the pool covered?')


class PoolLevel(IntEnum):
    Good = 1
    Bad  = 0


class PoolReading(models.Model):
    pool = models.ForeignKey(Pool, related_name='pool')
    when = models.DateTimeField()
    level = models.IntegerField(
        default=PoolLevel.Good,
        choices=[(l, l.name) for l in PoolLevel])
