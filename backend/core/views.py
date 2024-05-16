from django.shortcuts import render
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.response import Response
from urllib.parse import unquote as urlunquote
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Reference

from .models import *
from .serializers import *
from .permissions import *

class MachineBasicInfoFilter(filters.FilterSet):
    serial_number = filters.CharFilter(field_name='serial_number', lookup_expr='iexact')

    class Meta:
        model = MachineBasicInfo
        fields = ['serial_number']


class MachineBasicInfoViewSet(viewsets.ModelViewSet):
    queryset = MachineBasicInfo.objects.all()
    serializer_class = MachineBasicInfoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MachineBasicInfoFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ManagerPermission()]
        else:
            return [permissions.AllowAny()]


class MachineOwnershipInfoViewSet(viewsets.ModelViewSet):
    queryset = MachineOwnershipInfo.objects.all()
    serializer_class = MachineOwnershipInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['machine__serial_number']
    search_fields = ['machine__serial_number']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ManagerPermission()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_client:
                return MachineOwnershipInfo.objects.filter(client=user)
            elif user.is_service_company:
                return MachineOwnershipInfo.objects.filter(service_companies=user)
            elif user.is_manager:
                return MachineOwnershipInfo.objects.all()  # Менеджеры могут видеть все
        return MachineOwnershipInfo.objects.none()


class MachineDetailsViewSet(viewsets.ModelViewSet):
    queryset = MachineBasicInfo.objects.all()
    serializer_class = MachineDetailedInfoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ManagerPermission()]
        return [permissions.IsAuthenticated()]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [MaintenancePermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_client:
                return Maintenance.objects.filter(machine__ownership_info__client=user)
            elif user.is_service_company:
                return Maintenance.objects.filter(machine__ownership_info__service_companies=user)
        return super().get_queryset()

    

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [ClaimPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Claim.objects.all()
        elif user.is_service_company:
            return Claim.objects.filter(machine__ownership_info__service_companies=user)
        elif user.is_client:
            return Claim.objects.filter(machine__ownership_info__client=user)
        return Claim.objects.none()
    

class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsReferenceAccessible]

    def retrieve(self, request, *args, **kwargs):
        directory_name = request.resolver_match.kwargs.get('directory_name')
        name = request.resolver_match.kwargs.get('name')
        instance = get_object_or_404(Reference, directory_name=directory_name, name=name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



