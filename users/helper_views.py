from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated 


class AdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserView(APIView):
    permission_classes = [IsAuthenticated, IsNormalUser]