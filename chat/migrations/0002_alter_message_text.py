# Generated by Django 4.1.7 on 2023-02-27 18:23

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="text",
            field=djrichtextfield.models.RichTextField(),
        ),
    ]
