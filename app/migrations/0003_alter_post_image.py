# Generated by Django 4.2.6 on 2024-01-18 02:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_rename_profile_picture_userprofile_profile_pic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, max_length=350, null=True, upload_to="images"
            ),
        ),
    ]
