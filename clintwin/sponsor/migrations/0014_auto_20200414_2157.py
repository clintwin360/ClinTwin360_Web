# Generated by Django 3.0.4 on 2020-04-14 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0013_clinicaltrialmatch_match'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participantresponse',
            unique_together={('question', 'participant')},
        ),
    ]
