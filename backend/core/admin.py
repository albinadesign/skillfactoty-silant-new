from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.db.models import Q 

User = get_user_model()

class MachineBasicInfoAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'model_display', 'engine_model_display', 'engine_serial_number', 'transmission_model_display', 'transmission_serial_number', 'driving_axle_model_display', 'driving_axle_serial_number', 'steering_axle_model_display', 'steering_axle_serial_number']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        directory_fields = {
            'model': 'Модель техники',
            'engine_model': 'Модель двигателя',
            'transmission_model': 'Модель трансмиссии',
            'driving_axle_model': 'Модель ведущего моста',
            'steering_axle_model': 'Модель управляемого моста'
        }
        if db_field.name in directory_fields:
            kwargs["queryset"] = Reference.objects.filter(directory_name=directory_fields[db_field.name])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def model_display(self, obj):
        return obj.model.name if obj.model else '-'
    model_display.short_description = 'Model'

    def engine_model_display(self, obj):
        return obj.engine_model.name if obj.engine_model else '-'
    engine_model_display.short_description = 'Engine Model'

    def transmission_model_display(self, obj):
        return obj.transmission_model.name if obj.transmission_model else '-'
    transmission_model_display.short_description = 'Transmission Model'

    def driving_axle_model_display(self, obj):
        return obj.driving_axle_model.name if obj.driving_axle_model else '-'
    driving_axle_model_display.short_description = 'Driving Axle Model'

    def steering_axle_model_display(self, obj):
        return obj.steering_axle_model.name if obj.steering_axle_model else '-'
    steering_axle_model_display.short_description = 'Steering Axle Model'

    
    def has_change_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_superuser  # Менеджеры и суперпользователи могут изменять объекты

    def has_delete_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_superuser  # Менеджеры и суперпользователи могут удалять объекты
    
    def has_add_permission(self, request):
        return request.user.is_manager or request.user.is_superuser  # Менеджеры и суперпользователи могут добавлять объекты


class MachineOwnershipInfoAdmin(admin.ModelAdmin):
    list_filter = ['machine', 'shipment_date']
    list_display = ['machine', 'supply_contract_number', 'shipment_date', 'consignee', 'operation_address', 'configuration', 'client_display', 'service_companies_display']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            kwargs["queryset"] = User.objects.filter(is_client=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "service_companies":
            kwargs["queryset"] = User.objects.filter(is_service_company=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def client_display(self, obj):
        return obj.client.get_full_name() if obj.client else 'None'
    client_display.short_description = 'Client'

    def service_companies_display(self, obj):
        return ", ".join([sc.get_full_name() for sc in obj.service_companies.all()])
    service_companies_display.short_description = 'Service Companies'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_manager or request.user.is_superuser


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['machine', 'get_maintenance_type', 'date_performed', 'get_performing_organization']
    list_filter = ['maintenance_type', 'performing_organization', 'machine', 'date_performed']
    search_fields = ['machine__serial_number', 'order_number']
    fieldsets = (
        (None, {
            'fields': ('machine', 'maintenance_type', 'date_performed', 'hours_worked', 'order_number', 'order_date', 'performing_organization')
        }),
    )

    def get_maintenance_type(self, obj):
        return obj.maintenance_type.name if obj.maintenance_type else '-'
    get_maintenance_type.admin_order_field = 'maintenance_type'
    get_maintenance_type.short_description = 'Type of Maintenance'

    def get_performing_organization(self, obj):
        return obj.performing_organization.name if obj.performing_organization and obj.performing_organization.name != "Self-maintained" else 'Self-maintained'
    get_performing_organization.admin_order_field = 'performing_organization'
    get_performing_organization.short_description = 'Performed By'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "performing_organization":
            kwargs["queryset"] = Reference.objects.filter(Q(directory_name='Организация, проводившая ТО') | Q(name='Self-maintained'))
        elif db_field.name == "maintenance_type":
            kwargs["queryset"] = Reference.objects.filter(directory_name='Вид ТО')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def has_change_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_date', 'operating_hours', 'failure_node_display', 'failure_description', 'restoration_method_display', 'spare_parts_used', 'restoration_date', 'downtime')
    list_filter = ['machine', 'restoration_method', 'failure_date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        directory_mappings = {
            'failure_node': 'Узел отказа',
            'restoration_method': 'Способ восстановления'
        }
        if db_field.name in directory_mappings:
            kwargs["queryset"] = Reference.objects.filter(directory_name=directory_mappings[db_field.name])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def failure_node_display(self, obj):
        return obj.failure_node.name if obj.failure_node else 'None'
    failure_node_display.short_description = 'Failure node'

    def restoration_method_display(self, obj):
        return obj.restoration_method.name if obj.restoration_method else 'None'
    restoration_method_display.short_description = 'Restoration method'


    def has_change_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_manager or request.user.is_service_company or request.user.is_superuser

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['directory_name', 'name', 'description']
    list_filter = ['directory_name']
    search_fields = ['name', 'description']


admin.site.register(MachineBasicInfo, MachineBasicInfoAdmin)
admin.site.register(MachineOwnershipInfo, MachineOwnershipInfoAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Claim, ClaimAdmin)






