# Generated by Django 3.0.4 on 2020-04-08 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0007_questionschema_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuestionSchema',
        ),
    ]