# Generated by Django 3.2.5 on 2021-08-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='google_authenticator',
            field=models.BooleanField(default=False),
        ),
    ]
