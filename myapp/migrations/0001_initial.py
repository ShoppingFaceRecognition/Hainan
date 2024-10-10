# Generated by Django 4.2.11 on 2024-06-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Commodity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("number", models.IntegerField()),
                ("price", models.FloatField()),
                ("is_activity", models.BooleanField()),
                ("img", models.ImageField(upload_to="images/commodity")),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=150)),
                ("tel", models.IntegerField()),
                ("gender", models.BooleanField()),
                ("age", models.IntegerField()),
                ("view_difficult", models.BooleanField()),
                ("Consumption_frequency", models.IntegerField()),
                ("face_img_path", models.ImageField(upload_to="images/user/")),
            ],
        ),
    ]
