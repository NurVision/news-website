from rest_framework.permissions import BasePermission

class IsEditorOrAdmin(BasePermission):
    """
    Faqat Muharrir (EDITOR) yoki Administrator (ADMIN) rollariga ruxsat beradi.
    """
    def has_permission(self, request, view):
        # Avval autentifikatsiya tekshiruvi
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Keyin role maydoni mavjudligini tekshirish
        if not hasattr(request.user, 'role'):
            return False
        
        # Role to'g'ridan-to'g'ri tekshirish (katta harflarda)
        return request.user.role in ['ADMIN', 'EDITOR']