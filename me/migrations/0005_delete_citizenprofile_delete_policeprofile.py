# Generated by Django 4.2.2 on 2023-11-21 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0004_rename_las_name_policeprofile_last_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CitizenProfile',
        ),
        migrations.DeleteModel(
            name='Policeprofile',
        ),
    ]
