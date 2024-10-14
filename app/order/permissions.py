from rest_framework.permissions import BasePermission

class BranchAdminPermission(BasePermission):
    """
    Faqat 'branch_admin' roliga ega foydalanuvchilar ruxsat oladi
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'branch_admin')
