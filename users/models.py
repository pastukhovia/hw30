from django.contrib.auth.models import AbstractUser
from django.db import models

from locations.models import Location


class User(AbstractUser):
    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    MEMBER = 'member'
    ROLES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (MEMBER, MEMBER)
    ]

    role = models.CharField(max_length=9, choices=ROLES, default=MEMBER)
    age = models.IntegerField(default=0, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
