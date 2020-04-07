# Generated by Django 3.0.4 on 2020-03-26 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='participantquestionresponse',
            name='participant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sponsor.Participant'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='custom_id',
            field=models.CharField(max_length=100, null=True, verbose_name='Trial ID'),
        ),
    ]
