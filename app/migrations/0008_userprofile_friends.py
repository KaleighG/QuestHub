# Generated by Django 5.0 on 2024-01-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_friend_friend_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(to='app.userprofile'),
        ),
    ]
