# Generated by Django 3.2.20 on 2024-04-13 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0039_onboardingindicator_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardingindicator',
            name='step',
            field=models.CharField(choices=[('terms_of_use', 'Terms of Use'), ('Gaming Social Solutions By Paz Please Mark As Read', 'My Games Screen'), ('messages', 'Messages Screen'), ('profile_setup', 'Profile Setup'), ('notifications', 'Notifications Setup')], max_length=50),
        ),
        migrations.AlterField(
            model_name='onboardingindicator',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
