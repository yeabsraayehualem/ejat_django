from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class MyTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get('request'),
            username=phone,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid phone or password")

        # 🔑 Generate token manually (IMPORTANT)
        refresh = self.get_token(user)

        return {
            "id": user.id,
            "user": user.__str__(),
            "phone": user.phone,
            "role": "admin" if user.is_staff else "user",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }