# Generated by Django 5.1.4 on 2024-12-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0006_remove_book_in_reading_room"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookcard",
            name="isbn",
            field=models.CharField(max_length=18, unique=True),
        ),
    ]