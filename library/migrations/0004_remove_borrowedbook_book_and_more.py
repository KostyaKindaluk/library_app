# Generated by Django 5.1.4 on 2024-12-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_alter_reader_birthday_alter_reader_creation_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="borrowedbook",
            name="book",
        ),
        migrations.RemoveField(
            model_name="borrowedbook",
            name="borrow_date",
        ),
        migrations.RemoveField(
            model_name="borrowedbook",
            name="librarian",
        ),
        migrations.RemoveField(
            model_name="borrowedbook",
            name="reader",
        ),
        migrations.RemoveField(
            model_name="borrowedbook",
            name="return_until_date",
        ),
        migrations.AddField(
            model_name="borrowedbook",
            name="authors",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="borrowedbook",
            name="genre",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="borrowedbook",
            name="release_year",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="borrowedbook",
            name="title",
            field=models.CharField(max_length=200, null=True),
        ),
    ]