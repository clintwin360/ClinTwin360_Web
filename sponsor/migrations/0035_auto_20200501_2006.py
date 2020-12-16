# Generated by Django 3.0.4 on 2020-05-01 14:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import sponsor.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0034_sponsorrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='current_recruitment',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[sponsor.validators.validate_integer], verbose_name='Current Recruitment'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='enrollmentTarget',
            field=models.IntegerField(blank=True, null=True, validators=[sponsor.validators.validate_integer], verbose_name='Enrollment Target'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentEndDate',
            field=models.DateField(null=True, validators=[sponsor.validators.validate_date], verbose_name='Recruitment End Date'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='recruitmentStartDate',
            field=models.DateField(null=True, validators=[sponsor.validators.validate_date], verbose_name='Recruitment Start Date'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='status',
            field=models.CharField(default='Draft', max_length=100, null=True, validators=[sponsor.validators.validate_status], verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='url',
            field=models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator], verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='participant',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, validators=[sponsor.validators.validate_date]),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='participant',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='participantbasichealth',
            name='height',
            field=models.FloatField(null=True, validators=[sponsor.validators.validate_integer], verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='participantbasichealth',
            name='weight',
            field=models.FloatField(null=True, validators=[sponsor.validators.validate_integer], verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='dateDeregistered',
            field=models.DateField(blank=True, null=True, validators=[sponsor.validators.validate_date], verbose_name='Date of De-Regstration'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='date_joined',
            field=models.DateField(auto_now_add=True, null=True, validators=[sponsor.validators.validate_date], verbose_name='Date of Registration'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='email',
            field=models.EmailField(max_length=254, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sponsor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profiles', to='sponsor.Sponsor'),
        ),
    ]