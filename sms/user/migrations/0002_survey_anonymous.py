# Generated by Django 2.2.6 on 2019-10-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='anonymous',
            field=models.BooleanField(default=True),
        ),
    ]