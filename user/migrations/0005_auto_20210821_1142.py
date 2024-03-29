# Generated by Django 3.2.5 on 2021-08-21 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_authenticator_qrcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='authenticator_qrcode',
        ),
        migrations.CreateModel(
            name='UserQrcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authenticator_qrcode', models.ImageField(blank=True, null=True, upload_to='user_authenticator_qrcode_image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user_qrcode', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
