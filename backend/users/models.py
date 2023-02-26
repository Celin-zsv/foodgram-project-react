from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    username = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-ZА-Яа-я0-9_@+.-]{2,200}$',
            message=(
                'Username must be Alphanumeric: Latin /Rus leters, '
                'numbers, allowed _ @ + . - symbols, '
                'min 2 and max 200 symbols'),
            code='invalid_username'),
            RegexValidator(
                regex='[^me]',
                message=('Is not allowed username "me"'),
                code='invalid_username me')],
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Имя',
        default='not known first_name'
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Фамилия',
        default='not known last_name'
    )
    password = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
        verbose_name='Пароль'
    )
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    USERNAME_FIELD = 'email'


class Subscription(models.Model):
    following = models.ForeignKey(  # on whom
        User, on_delete=models.CASCADE, related_name='subscriptions_following')
    user = models.ForeignKey(  # who
        User, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self) -> str:
        return f'{self.user}. {self.following}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_following_user'
            ),
            models.CheckConstraint(
                name='user_equal_following',
                check=~models.Q(
                    user=models.F('following')
                    )
            )
        ]
