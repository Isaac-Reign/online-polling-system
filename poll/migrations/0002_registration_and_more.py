# Generated by Django 4.1.5 on 2023-01-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('foget_pass', models.CharField(blank=True, max_length=200, null=True)),
                ('password', models.CharField(max_length=30)),
                ('confirm_password', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='completeregistration',
            name='profile_picture',
            field=models.ImageField(upload_to=''),
        ),
    ]
