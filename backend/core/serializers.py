from rest_framework import serializers
from .models import MachineBasicInfo, MachineOwnershipInfo, Maintenance, Claim, Reference
from rest_framework.fields import SerializerMethodField
from accounts.serializers import *

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['directory_name', 'name', 'description']
        
class MachineBasicInfoSerializer(serializers.ModelSerializer):
    model = ReferenceSerializer(read_only=True)
    engine_model = ReferenceSerializer(read_only=True)
    transmission_model = ReferenceSerializer(read_only=True)
    driving_axle_model = ReferenceSerializer(read_only=True)
    steering_axle_model = ReferenceSerializer(read_only=True)

    class Meta:
        model = MachineBasicInfo
        fields = [
            'serial_number',
            'model',
            'engine_model',
            'engine_serial_number',
            'transmission_model',
            'transmission_serial_number',
            'driving_axle_model',
            'driving_axle_serial_number',
            'steering_axle_model',
            'steering_axle_serial_number'
        ]
    

class MachineOwnershipInfoSerializer(serializers.ModelSerializer):
    machine = MachineBasicInfoSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    service_companies = serializers.SerializerMethodField()

    def get_service_companies(self, obj):
        return [company.username for company in obj.service_companies.all()]

    class Meta:
        model = MachineOwnershipInfo
        fields = [
            'machine', 'supply_contract_number', 'shipment_date', 'client', 'service_companies'
        ]

    def get_detailed_info(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if request.user.is_client and obj.client == request.user:
                return {
                    'consignee': obj.consignee,
                    'operation_address': obj.operation_address,
                    'configuration': obj.configuration
                }
            elif request.user.is_service_company and obj.service_companies.filter(user=request.user).exists():
                return {
                    'consignee': obj.consignee,
                    'operation_address': obj.operation_address
                }
        return None
    

class MachineDetailedInfoSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField()
    model_name = serializers.CharField(source='model.name')
    engine_model_name = serializers.CharField(source='engine_model.name')
    engine_serial_number = serializers.CharField()
    transmission_model_name = serializers.CharField(source='transmission_model.name')
    transmission_serial_number = serializers.CharField()
    driving_axle_model_name = serializers.CharField(source='driving_axle_model.name')
    driving_axle_serial_number = serializers.CharField()
    steering_axle_model_name = serializers.CharField(source='steering_axle_model.name')
    steering_axle_serial_number = serializers.CharField()
    client = serializers.SerializerMethodField()
    consignee = serializers.SerializerMethodField()
    shipment_date = serializers.SerializerMethodField()
    operation_address = serializers.SerializerMethodField()
    configuration = serializers.SerializerMethodField()
    service_companies = serializers.SerializerMethodField()

    def get_client(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return obj.ownership_info.client.last_name if obj.ownership_info.client else '-----'
        return '-----'

    def get_consignee(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return obj.ownership_info.consignee if obj.ownership_info.consignee else '-----'
        return '-----'

    def get_shipment_date(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return obj.ownership_info.shipment_date if obj.ownership_info.shipment_date else '-----'
        return '-----'

    def get_operation_address(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return obj.ownership_info.operation_address if obj.ownership_info.operation_address else '-----'
        return '-----'

    def get_configuration(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return obj.ownership_info.configuration if obj.ownership_info.configuration else '-----'
        return '-----'

    def get_service_companies(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated and (
            request.user.is_manager or
            (request.user.is_client and obj.ownership_info.client == request.user) or
            (request.user.is_service_company and request.user in obj.ownership_info.service_companies.all())
        ):
            return [company.last_name for company in obj.ownership_info.service_companies.all()] if obj.ownership_info.service_companies.exists() else ['-----']
        return ['-----']

    class Meta:
        model = MachineBasicInfo
        fields = [
            'serial_number', 'model_name', 'engine_model_name', 'engine_serial_number',
            'transmission_model_name', 'transmission_serial_number', 'driving_axle_model_name',
            'driving_axle_serial_number', 'steering_axle_model_name', 'steering_axle_serial_number',
            'client', 'consignee', 'shipment_date', 'operation_address', 'configuration', 'service_companies'
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    machine_serial_number = serializers.CharField(source='machine.serial_number')
    maintenance_type_name = serializers.CharField(source='maintenance_type.name')
    performing_organization_name = serializers.CharField(source='performing_organization.name')
    client = serializers.CharField(source='machine.ownership_info.client.username')
    service_companies = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = [
            'machine_serial_number', 
            'maintenance_type_name', 
            'date_performed', 
            'hours_worked', 
            'order_number', 
            'order_date', 
            'performing_organization_name',
            'client',
            'service_companies'
        ]

    def get_service_companies(self, obj):
        return [company.username for company in obj.machine.ownership_info.service_companies.all()]

    

class ClaimSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField(source='machine.serial_number', read_only=True)
    client = serializers.CharField(source='machine.ownership_info.client.username', read_only=True)
    service_companies = serializers.SerializerMethodField()
    failure_node = serializers.CharField(source='failure_node.name', read_only=True)
    restoration_method = serializers.CharField(source='restoration_method.name', read_only=True)

    def get_service_companies(self, obj):
        return [{'username': company.username, 'last_name': company.last_name} for company in obj.machine.ownership_info.service_companies.all()]

    class Meta:
        model = Claim
        fields = [
            'id', 'serial_number', 'failure_date', 'operating_hours', 'failure_node', 
            'failure_description', 'restoration_method', 'spare_parts_used', 
            'restoration_date', 'downtime', 'client', 'service_companies'
        ]




        

    