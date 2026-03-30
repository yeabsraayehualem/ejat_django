from django.shortcuts import render
from rest_framework.response import Response
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from users.helper_views import UserView

# Create your views here.
class GetAttendancesView(UserView):
    
    def get(self, request):
        attendances = Attendance.objects.filter(name=request.user)
        data = {
            "present": attendances.filter(status='p').count(),
            "absent": attendances.filter(status='a').count(),
        }
        return Response(data)
    
    def post(self, request):
        # data = request.data
        attendance = Attendance.objects.create(
            name=request.user,
            status='p'
        )
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)