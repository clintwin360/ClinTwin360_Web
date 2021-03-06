# Generated by Django 3.0.4 on 2020-05-13 15:20

from django.db import migrations, models
import sponsor.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0050_auto_20200512_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicaltrial',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Active Recruitment', 'Active Recruitment'), ('Recruitment Ended', 'Recruitment Ended')], default='Draft', max_length=100, null=True, validators=[sponsor.validators.validate_status], verbose_name='Status'),
        ),
    ]
