# Generated by Django 2.0.6 on 2018-06-02 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, validators=[django.core.validators.URLValidator])),
                ('shrtzy', models.URLField(unique=True, validators=[django.core.validators.URLValidator])),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
