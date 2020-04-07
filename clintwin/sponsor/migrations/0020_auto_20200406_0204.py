# Generated by Django 3.0.4 on 2020-04-06 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0019_auto_20200406_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='dateBirth',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='date_deregistered',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='height',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='weight',
        ),
        migrations.AlterField(
            model_name='participant',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='participant',
            name='first_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='last_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='phone',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.CreateModel(
            name='ParticipantBasicHealth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True, verbose_name='Gender')),
                ('weight', models.FloatField(null=True, verbose_name='Weight')),
                ('height', models.FloatField(null=True, verbose_name='Height')),
                ('birth_date', models.DateField(blank=True, help_text='MM/DD/YY', null=True, verbose_name='Date of Birth')),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sponsor.Participant')),
            ],
        ),
    ]
