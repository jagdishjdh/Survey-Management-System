# Generated by Django 2.2.6 on 2019-11-14 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191114_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='q_type',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
