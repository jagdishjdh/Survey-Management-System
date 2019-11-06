

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('q_type', models.CharField(max_length=100)),
                ('required', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('endDate', models.DateTimeField(blank=True, default=None, null=True)),
                ('isopen', models.BooleanField(default=True)),
                ('anonymous', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.BooleanField(default=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_no', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Options')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Section'),
        ),
        migrations.AddField(
            model_name='options',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Question'),
        ),
    ]
