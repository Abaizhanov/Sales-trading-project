from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Доступ только для администраторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrader(permissions.BasePermission):
    """
    Доступ только для трейдеров.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trader'

class IsSalesRep(permissions.BasePermission):
    """
    Доступ только для Sales Representative.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_rep'
