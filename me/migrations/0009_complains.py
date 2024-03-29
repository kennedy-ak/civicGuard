# Generated by Django 4.2.2 on 2023-11-24 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0008_rename_driver_linence_image_front_citizenprofile_driver_license_image_front_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('region', models.CharField(max_length=30)),
                ('land_mark', models.CharField(max_length=50)),
                ('fine_paid', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='me.citizenprofile')),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='me.policeprofile')),
            ],
        ),
    ]
