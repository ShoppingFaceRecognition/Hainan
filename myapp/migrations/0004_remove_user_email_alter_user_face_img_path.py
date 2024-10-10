# Generated by Django 4.2.11 on 2024-06-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_user_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="email",
        ),
        migrations.AlterField(
            model_name="user",
            name="face_img_path",
            field=models.ImageField(null=True, upload_to="images/user/"),
        ),
    ]
