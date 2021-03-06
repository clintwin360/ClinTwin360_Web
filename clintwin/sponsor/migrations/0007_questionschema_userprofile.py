# Generated by Django 3.0.4 on 2020-04-08 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sponsor', '0006_auto_20200408_0428'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sponsor.Sponsor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
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
