# Generated by Django 4.2.1 on 2023-06-04 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="age",
            field=models.PositiveIntegerField(
                blank=True, help_text="User age", null=True, verbose_name="User age"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "male"), ("female", "female"), ("other", "other")],
                help_text="User gender",
                max_length=20,
                null=True,
                verbose_name="User gender",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="website",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]