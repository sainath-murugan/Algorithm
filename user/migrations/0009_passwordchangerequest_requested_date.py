# Generated by Django 3.2.5 on 2021-08-21 12:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_customuser_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordchangerequest',
            name='requested_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]