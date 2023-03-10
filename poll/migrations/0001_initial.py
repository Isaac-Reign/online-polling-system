# Generated by Django 4.1.5 on 2023-01-17 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSitting1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_vote', models.BooleanField(default=False)),
                ('registration_complete', models.BooleanField(default=False)),
                ('show_results', models.BooleanField(default=False)),
                ('be_inform', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_position', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_course', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_range', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=200)),
                ('vote_count', models.IntegerField(default=0)),
                ('person_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('have_vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('person_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.studentcourse')),
                ('person_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.position')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompleteRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default=0, max_length=10)),
                ('profile_picture', models.ImageField(upload_to='pics')),
                ('can_vote', models.BooleanField(default=True)),
                ('relation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student_range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.studentrange')),
                ('your_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.studentcourse')),
            ],
        ),
    ]
