# Generated by Django 4.1.1 on 2024-04-25 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_reference_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineBasicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('engine_serial_number', models.CharField(max_length=100)),
                ('transmission_serial_number', models.CharField(max_length=100)),
                ('driving_axle_serial_number', models.CharField(max_length=100)),
                ('steering_axle_serial_number', models.CharField(max_length=100)),
                ('driving_axle_model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='machines_driving_axle_basic', to='core.reference')),
                ('engine_model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='machines_engine_basic', to='core.reference')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='machines_model_basic', to='core.reference')),
                ('steering_axle_model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='machines_steering_axle_basic', to='core.reference')),
                ('transmission_model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='machines_transmission_basic', to='core.reference')),
            ],
        ),
        migrations.CreateModel(
            name='MachineOwnershipInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supply_contract_number', models.CharField(max_length=100)),
                ('shipment_date', models.DateField()),
                ('consignee', models.CharField(max_length=100)),
                ('operation_address', models.CharField(max_length=200)),
                ('configuration', models.TextField()),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_machines', to='core.client')),
                ('machine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ownership_info', to='core.machinebasicinfo')),
                ('service_companies', models.ManyToManyField(related_name='serviced_machines', to='core.servicecompany')),
            ],
        ),
        migrations.AlterField(
            model_name='claim',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='core.machinebasicinfo'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenances', to='core.machinebasicinfo'),
        ),
        migrations.DeleteModel(
            name='Machine',
        ),
    ]
