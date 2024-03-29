# Generated by Django 3.0.4 on 2020-05-07 03:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sponsor', '0044_auto_20200507_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantprofile',
            name='participant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='sponsor.Participant'),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='participant_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
