# Generated by Django 4.2.11 on 2024-06-27 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
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
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.CharField(default="123@example.com", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="fen",
            field=models.IntegerField(default="1"),
            preserve_default=False,
        ),
    ]
