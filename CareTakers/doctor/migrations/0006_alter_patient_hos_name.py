# Generated by Django 4.0.4 on 2022-05-07 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='hos_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
