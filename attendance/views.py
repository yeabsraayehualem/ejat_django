from datetime import datetime
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from users.helper_views import UserView
from datetime import datetime
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
        data = request.data
        # print(data)
        # print(request.user)
        attendance = Attendance.objects.filter(name=request.user, date=datetime.now().date())
        if attendance:
            return Response({
                "status":"success",
                "message": "You have already marked your attendance"
            })

        attendance = Attendance.objects.create(
            name=request.user,
            status='p'
        )
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

class AllMyAttendandancesView(UserView):
    
    def get(self, request):
        attendances = Attendance.objects.filter(name=request.user).order_by('-id')
        data = [{
            'id': attendance.id,
            'status': "present" if attendance.status == 'p' else "absent",
            'date': attendance.date.strftime("%Y-%m-%d")
        } for attendance in attendances]
        return Response(data)