# Generated by Django 2.2.16 on 2023-02-15 10:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Наименование')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество в рецепте')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Наименование')),
                ('text', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(default=None, null=True, upload_to='recipes/images/')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Наименование')),
                ('color', models.CharField(max_length=7, verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(max_length=200, null=True, verbose_name='Слаг')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Tag')),
            ],
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('slug',), name='unique_slug'),
        ),
        migrations.AddField(
            model_name='shopping',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppings', to='recipes.Recipe'),
        ),
    ]