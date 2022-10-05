# Generated by Django 4.0.4 on 2022-05-07 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_prediction'),
    ]

    operations = [
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=25)),
                ('status', models.CharField(max_length=50)),
                ('illness', models.TextField(blank=True, null=True)),
                ('doctor_select', models.TextField(default='Vivek')),
                ('hos_name', models.CharField(max_length=50)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('med_cost', models.IntegerField(blank=True, null=True)),
                ('discount_cost', models.IntegerField(blank=True, null=True)),
                ('total_cost', models.IntegerField(blank=True, null=True)),
                ('blood_test', models.BooleanField(blank=True, null=True)),
                ('general_checkup', models.BooleanField(blank=True, null=True)),
                ('chest_xray', models.BooleanField(blank=True, null=True)),
                ('ct_scan', models.BooleanField(blank=True, null=True)),
                ('dental_treatment', models.BooleanField(blank=True, null=True)),
                ('ET_Treatment', models.BooleanField(blank=True, null=True)),
                ('Full_checkup', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]
