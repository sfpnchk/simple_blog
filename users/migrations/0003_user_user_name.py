# Generated by Django 4.2.1 on 2023-06-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_address_user_age_user_gender_user_website_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_name",
            field=models.CharField(default="def", max_length=30, unique=True),
            preserve_default=False,
        ),
    ]