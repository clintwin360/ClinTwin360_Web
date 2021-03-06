# Generated by Django 3.0.4 on 2020-04-25 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0025_auto_20200424_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentEndDate',
            field=models.DateField(help_text='MM/DD/YYYY', null=True, verbose_name='Recruitment End Date'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentStartDate',
            field=models.DateField(help_text='MM/DD/YYYY', null=True, verbose_name='Recruitment Start Date'),
        ),
    ]
