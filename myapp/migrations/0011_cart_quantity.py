# Generated by Django 4.2.11 on 2024-07-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0010_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="quantity",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
