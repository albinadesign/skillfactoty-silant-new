# Generated by Django 4.1.1 on 2024-05-08 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_maintenance_performing_organization_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='self_maintained',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='service_company',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='performing_organization',
            field=models.ForeignKey(blank=True, limit_choices_to={'directory_name': 'Организация, проводившая ТО'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='maintenance_service_companies', to='core.reference'),
        ),
    ]