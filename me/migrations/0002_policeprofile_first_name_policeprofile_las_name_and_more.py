# Generated by Django 4.2.6 on 2023-11-21 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='policeprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='policeprofile',
            name='las_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='policeprofile',
            name='rank',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
