# Generated by Django 3.2.5 on 2021-08-21 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210821_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userqrcode',
            name='user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='qr_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_user_qrcode', to='user.userqrcode'),
        ),
    ]
