# Generated by Django 3.2.5 on 2021-08-20 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_passwordchangerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='authenticator_qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='user_authenticator_qrcode_image'),
        ),
    ]
