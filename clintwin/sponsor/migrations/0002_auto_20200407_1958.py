# Generated by Django 3.0.4 on 2020-04-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='title',
            field=models.CharField(max_length=500, null=True, verbose_name='Trial Title'),
        ),
    ]
