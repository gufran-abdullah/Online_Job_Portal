# Generated by Django 3.0.6 on 2021-06-18 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_userapply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userapply',
            name='job',
        ),
    ]
