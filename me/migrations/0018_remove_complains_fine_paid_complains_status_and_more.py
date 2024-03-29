# Generated by Django 4.2.2 on 2023-12-15 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0017_merge_20231204_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complains',
            name='fine_paid',
        ),
        migrations.AddField(
            model_name='complains',
            name='status',
            field=models.CharField(blank=True, choices=[('pending_payment', 'Pending'), ('fine_paid', 'Paid')], default='pending_payment', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='citizenprofile',
            name='driver_license_Image_front',
            field=models.ImageField(blank=True, null=True, upload_to='drivers_linence_Image/'),
        ),
    ]
