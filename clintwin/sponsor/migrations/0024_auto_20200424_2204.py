# Generated by Django 3.0.4 on 2020-04-24 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0023_auto_20200424_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantquestion',
            name='trial_id',
        ),
        migrations.RemoveField(
            model_name='participantresponse',
            name='trial_id',
        ),
    ]