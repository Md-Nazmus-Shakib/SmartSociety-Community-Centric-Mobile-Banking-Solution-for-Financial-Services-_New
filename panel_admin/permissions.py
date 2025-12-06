from rest_framework.permissions import BasePermission

class IsPanelAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.session.get("panel_admin_id"))