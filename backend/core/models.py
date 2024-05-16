from django.db import models
from accounts.models import *


class Reference(models.Model):
    directory_name = models.CharField(max_length=100)  # Название справочника
    name = models.CharField(max_length=100)            # Название элемента справочника
    description = models.TextField(blank=True, null=True) # Описание элемента

    class Meta:
        unique_together = ('directory_name', 'name')

    def __str__(self):
        return f"{self.directory_name}: {self.name}"
    

class MachineBasicInfo(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)  # Зав. № машины
    model = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='machines_model_basic', limit_choices_to={'directory_name': 'Модель техники'})  # Модель техники из справочника
    engine_model = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='machines_engine_basic', limit_choices_to={'directory_name': 'Модель двигателя'})  # Модель двигателя из справочника
    engine_serial_number = models.CharField(max_length=100)  # Зав. № двигателя
    transmission_model = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='machines_transmission_basic', limit_choices_to={'directory_name': 'Модель трансмиссии'})  # Модель трансмиссии из справочника
    transmission_serial_number = models.CharField(max_length=100)  # Зав. № трансмиссии
    driving_axle_model = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='machines_driving_axle_basic', limit_choices_to={'directory_name': 'Модель ведущего моста'})  # Модель ведущего моста из справочника
    driving_axle_serial_number = models.CharField(max_length=100)  # Зав. № ведущего моста
    steering_axle_model = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='machines_steering_axle_basic', limit_choices_to={'directory_name': 'Модель управляемого моста'})  # Модель управляемого моста из справочника
    steering_axle_serial_number = models.CharField(max_length=100)  # Зав. № управляемого моста

    def __str__(self):
        return self.serial_number
    

class MachineOwnershipInfo(models.Model):
    machine = models.OneToOneField(MachineBasicInfo, on_delete=models.CASCADE, related_name='ownership_info')
    supply_contract_number = models.CharField(max_length=100)  # Договор поставки №, дата
    shipment_date = models.DateField()  # Дата отгрузки с завода
    consignee = models.CharField(max_length=100)  # Грузополучатель (конечный потребитель)
    operation_address = models.CharField(max_length=200)  # Адрес поставки (эксплуатации)
    configuration = models.TextField()  # Комплектация (доп. опции)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_machines', limit_choices_to={'is_client': True})  # Клиент
    service_companies = models.ManyToManyField(User, related_name='serviced_machines', limit_choices_to={'is_service_company': True})  # Сервисные компании

    def __str__(self):
        return f"{self.machine.serial_number} - Ownership Info"
    

class Maintenance(models.Model):
    machine = models.ForeignKey(MachineBasicInfo, on_delete=models.CASCADE, related_name='maintenances')  # Машина
    maintenance_type = models.ForeignKey(Reference, on_delete=models.RESTRICT, related_name='maintenances_type', limit_choices_to={'directory_name': 'Вид ТО'})
    date_performed = models.DateField()  # Дата проведения ТО
    hours_worked = models.IntegerField()  # Наработка, м/час
    order_number = models.CharField(max_length=100)  # № заказ-наряда
    order_date = models.DateField()  # Дата заказ-наряда
    performing_organization = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.RESTRICT, related_name='maintenance_service_companies', limit_choices_to={'directory_name': 'Организация, проводившая ТО'})  # Организация, проводившая ТО
    
    def __str__(self):
        maintenance_type_name = self.maintenance_type.name if self.maintenance_type else 'Unknown'
        performing_org_name = self.performing_organization.name if self.performing_organization else 'Unknown'
        return f"{maintenance_type_name} on {self.date_performed} by {performing_org_name}"
    

class Claim(models.Model):
    machine = models.ForeignKey(MachineBasicInfo, on_delete=models.CASCADE, related_name='claims')  # Машина
    failure_date = models.DateField()  # Дата отказа
    operating_hours = models.IntegerField()  # Наработка, м/час
    failure_node = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.RESTRICT, related_name='claim_failure_nodes', limit_choices_to={'directory_name': 'Узел отказа'})  # Узел отказа из справочника
    failure_description = models.TextField()  # Описание отказа
    restoration_method = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.RESTRICT, related_name='claim_restoration_methods', limit_choices_to={'directory_name': 'Способ восстановления'})  # Способ восстановления из справочника
    spare_parts_used = models.TextField(blank=True, null=True)  # Используемые запасные части
    restoration_date = models.DateField()  # Дата восстановления
    downtime = models.IntegerField(editable=False)  # Время простоя техники, расчетное поле
    
    def __str__(self):
        return f"{self.failure_node} - {self.failure_date}"

    def save(self, *args, **kwargs):
        if self.restoration_date and self.failure_date:
            self.downtime = (self.restoration_date - self.failure_date).days
        super().save(*args, **kwargs)
