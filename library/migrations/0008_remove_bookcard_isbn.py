# Generated by Django 5.1.4 on 2024-12-29 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0007_alter_bookcard_isbn"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bookcard",
            name="isbn",
        ),
    ]