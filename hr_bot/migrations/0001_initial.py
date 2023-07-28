# Generated by Django 3.0.7 on 2021-03-10 07:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import its_utils.app_telegram_bot.models.abstract_message


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HrBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('auth_token', models.CharField(default='', max_length=100)),
                ('last_update_id', models.IntegerField(blank=True, default=0)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HrChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=100)),
                ('telegram_type', models.CharField(blank=True, choices=[('private', 'private'), ('group', 'group'), ('supergroup', 'supergroup')], default='', max_length=25, null=True)),
                ('secret', models.CharField(blank=True, default='', max_length=50)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hr_bot.HrBot')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HrUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=100)),
                ('username', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=127, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=127, null=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HrMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField()),
                ('text', models.TextField(default='', null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('voice', models.FileField(blank=True, null=True, upload_to=its_utils.app_telegram_bot.models.abstract_message.voice_upload_path)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hr_bot.HrUser')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='hr_bot.HrChat')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HrChatParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='hr_bot.HrChat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participated_chats', to='hr_bot.HrUser')),
            ],
            options={
                'verbose_name': 'Участник чата',
                'verbose_name_plural': 'Участники чатов',
                'abstract': False,
                'unique_together': {('chat', 'user')},
            },
        ),
    ]