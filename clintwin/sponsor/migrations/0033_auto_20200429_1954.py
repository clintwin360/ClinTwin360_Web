# Generated by Django 3.0.4 on 2020-04-29 19:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0032_auto_20200429_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushnotification',
            name='createdTimeStamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='sendResponse',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
