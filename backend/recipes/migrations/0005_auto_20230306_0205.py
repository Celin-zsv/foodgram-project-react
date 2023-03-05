# Generated by Django 2.2.16 on 2023-03-05 23:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230306_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=200, validators=[django.core.validators.RegexValidator(message='В наименовании запрещены символы: $%^&#:;!', regex='^[^$%^&#:;!]+$')], verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(db_index=True, max_length=200, validators=[django.core.validators.RegexValidator(message='В наименовании запрещены символы: $%^&#:;!', regex='^[^$%^&#:;!]+$')], verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=200, validators=[django.core.validators.RegexValidator(message='В наименовании запрещены символы: $%^&#:;!', regex='^[^$%^&#:;!]+$')], verbose_name='Наименование'),
        ),
    ]
