from rest_framework import permissions

class ClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user

class ServiceCompanyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_service_company

    def has_object_permission(self, request, view, obj):
        return request.user in obj.service_companies.all()

class ManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

    def has_object_permission(self, request, view, obj):
        return True

class DetailedViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_client or request.user.is_service_company or request.user.is_manager)

    def has_object_permission(self, request, view, obj):
        return request.user.is_manager or request.user.is_service_company or obj.client == request.user

    

class MaintenancePermission(permissions.BasePermission):
    """
    Определяет разрешения для модели Maintenance в зависимости от роли пользователя.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован для любых действий
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'retrieve', 'create']:
            return True  # Все аутентифицированные пользователи могут просматривать и создавать записи ТО

        # Изменение и удаление данных разрешено только сервисным компаниям и менеджерам
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_service_company or request.user.is_manager

        return False

    def has_object_permission(self, request, view, obj):
        # Клиенты могут просматривать и создавать записи ТО только для своих машин, не могут изменять или удалять
        if view.action in ['retrieve', 'create']:
            return obj.machine.client == request.user.client_profile if request.user.is_client else False

        # Сервисные компании могут изменять ТО, если они обслуживают данную машину
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.service_company_profile == obj.service_company if request.user.is_service_company else False

        # Менеджеры имеют полный доступ ко всем операциям
        return request.user.is_manager
    

class ClaimPermission(permissions.BasePermission):
    """
    Определяет разрешения для модели Claim в зависимости от роли пользователя.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован для любых действий
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'retrieve']:
            return True  # Все аутентифицированные пользователи могут просматривать рекламации

        # Создание и изменение данных разрешено только сервисным компаниям и менеджерам
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_service_company or request.user.is_manager

        return False

    def has_object_permission(self, request, view, obj):
        # Клиенты могут просматривать рекламации только своих машин
        if view.action in ['retrieve']:
            return obj.machine.client == request.user.client_profile if request.user.is_client else False

        # Сервисные компании могут изменять рекламации, если они обслуживают данную машину
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.service_company_profile == obj.service_company if request.user.is_service_company else False

        # Менеджеры имеют полный доступ ко всем операциям
        return request.user.is_manager
    

class IsReferenceAccessible(permissions.BasePermission):
    def has_permission(self, request, view):
        public_directories = ['Модель техники', 'Модель двигателя', 'Модель трансмиссии', 'Модель ведущего моста', 'Модель управляемого моста']
        directory_name = request.resolver_match.kwargs.get('directory_name')

        if directory_name in public_directories:
            return True  # Доступно всем
        return request.user.is_authenticated  # Только зарегистрированным пользователям
