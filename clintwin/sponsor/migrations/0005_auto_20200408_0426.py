# Generated by Django 3.0.4 on 2020-04-08 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0004_auto_20200408_0329'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='clinicaltrial',
            name='title',
            field=models.CharField(max_length=1000, null=True, verbose_name='Trial Title'),
        ),
    ]
