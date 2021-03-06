# Generated by Django 3.0.4 on 2020-04-23 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0020_virtualtrialparticipantquestion_virtualtrialparticipantresponse'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='virtualtrialparticipantresponse',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='virtualtrialparticipantresponse',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='virtualtrialparticipantresponse',
            name='question',
        ),
        migrations.DeleteModel(
            name='VirtualTrialParticipantQuestion',
        ),
        migrations.DeleteModel(
            name='VirtualTrialParticipantResponse',
        ),
    ]
