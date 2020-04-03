# Generated by Django 3.0.4 on 2020-04-03 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0012_auto_20200402_0214'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='dateBirth',
            field=models.DateField(blank=True, help_text='MM/DD/YY', null=True, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='participant',
            name='date_deregistered',
            field=models.DateField(blank=True, help_text='MM/DD/YY', null=True, verbose_name='Date of De-Registration'),
        ),
        migrations.AddField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default=None, max_length=1, verbose_name='Gender'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='height',
            field=models.FloatField(default=None, verbose_name='Height'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='location',
            field=models.CharField(default=None, max_length=100, verbose_name='Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='phone',
            field=models.IntegerField(default=None, verbose_name='Phone'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='weight',
            field=models.FloatField(default=None, verbose_name='Weight'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participant',
            name='date_joined',
            field=models.DateField(blank=True, help_text='MM/DD/YY', null=True, verbose_name='Date of Registration'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Lasst Name'),
        ),
        migrations.CreateModel(
            name='QuestionSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionText', models.TextField(blank=True, null=True, verbose_name='Question Text')),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Type')),
                ('nextQuestion', models.CharField(blank=True, max_length=30, null=True, verbose_name='Next Question')),
                ('criteria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sponsor.ClinicalTrialCriteria')),
                ('responseId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sponsor.ClinicalTrialCriteriaResponse')),
            ],
        ),
    ]
