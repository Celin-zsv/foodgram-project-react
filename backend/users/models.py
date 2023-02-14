from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (GUEST, 'guest'),
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        default='not knowen'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
        verbose_name='Пароль'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='user',
        verbose_name='Уровень доступа'
    )
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    USERNAME_FIELD = 'email'


class Subscription(models.Model):
    following_id = models.ForeignKey(  # на кого подписываются
        User, on_delete=models.CASCADE, related_name='subscriptions_following')
    user = models.ForeignKey(  # кто подписывается
        User, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self) -> str:
        return f'{self.user}. {self.following_id}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following_id', 'user'],
                name='unique_following_user'
            )
        ]
