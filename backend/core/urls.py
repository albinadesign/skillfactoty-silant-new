from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Silant API",
        default_version='v1',
        description="API documentation for Silant application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'machines', MachineBasicInfoViewSet)
router.register(r'ownership', MachineOwnershipInfoViewSet)
router.register(r'maintenance', MaintenanceViewSet)
router.register(r'claims', ClaimViewSet)
router.register(r'references/(?P<directory_name>.+)/(?P<name>.+)', ReferenceViewSet, basename='reference')
router.register(r'machine_details', MachineDetailsViewSet, basename='machine-details')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]