# Generated by Django 5.1.1 on 2024-09-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="corner",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]