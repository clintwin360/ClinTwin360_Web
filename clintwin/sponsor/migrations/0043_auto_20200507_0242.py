# Generated by Django 3.0.4 on 2020-05-07 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0042_merge_20200505_0333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='basic_health',
        ),
        migrations.AlterField(
            model_name='participantbasichealth',
            name='participant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basic_health', to='sponsor.Participant'),
        ),
    ]
