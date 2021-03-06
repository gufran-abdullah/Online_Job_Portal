# Generated by Django 3.0.6 on 2021-06-17 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_recruiter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=300)),
                ('salary', models.FloatField(max_length=20)),
                ('experience', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('skills', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('creation_date', models.DateField()),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Recruiter')),
            ],
        ),
    ]
