# Generated by Django 4.2.6 on 2023-10-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescriptions', '0002_alter_dosechecking_checked_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_weight',
            field=models.CharField(default='unknown', max_length=255),
        ),
    ]