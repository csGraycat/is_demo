# Generated by Django 4.2.13 on 2024-05-31 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callsuploader', '0003_callinfo_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callinfo',
            name='vote',
            field=models.IntegerField(blank=True, choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], null=True),
        ),
    ]
