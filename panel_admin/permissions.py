from rest_framework.permissions import BasePermission
from .models import PanelAdmin

class IsPanelAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        admin_id = request.session.get("panel_admin_id")
        if not admin_id:
            return False

        # attach admin to request
        try:
            request.panel_admin = PanelAdmin.objects.get(id=admin_id)
            return True
        except PanelAdmin.DoesNotExist:
            return False
