# Generated by Django 3.0.4 on 2020-05-04 04:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0039_sponsorrequest_createdat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='current_recruitment',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0, 'You can not enter a negative value')], verbose_name='Current Recruitment'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='enrollmentTarget',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'You can not enter a negative value')], verbose_name='Enrollment Target'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentEndDate',
            field=models.DateField(null=True, verbose_name='Recruitment End Date'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentStartDate',
            field=models.DateField(null=True, verbose_name='Recruitment Start Date'),
        ),
        migrations.AlterField(
            model_name='participantbasichealth',
            name='height',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'You can not enter a negative value')], verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='participantbasichealth',
            name='weight',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0, 'You can not enter a negative value')], verbose_name='Weight'),
        ),
    ]
