# Generated by Django 3.0.6 on 2021-06-16 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20210616_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentuser',
            name='image',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
