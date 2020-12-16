# Generated by Django 3.0.4 on 2020-04-25 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0026_auto_20200425_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='is_virtual',
            field=models.BooleanField(help_text='Do you plan to administer this trial purely online?', null=True, verbose_name='Virtual Trial'),
        ),
    ]