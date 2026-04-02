from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenSerializer
from .helper_views import AdminView
from .models import Account,Department, SecularTitle, SpiritualTitle
from attendance.models import Attendance
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt


class JWTAuthCustom(TokenObtainPairView):
    serializer_class = MyTokenSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def check_user(request):
    data = request.data
    phone = data.get("phone")

    try:
        user = Account.objects.get(phone=phone)
    except Account.DoesNotExist:
        return Response({"message": "User does not exist"}, status=404)

    if not user.password or len(user.password) < 3:
        return Response({"login": False, "message": "User has no last login", "user_id": user.id}, status=200)

    return Response({"login": True}, status=200)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def set_password(request):
    data = request.data
    phone = data.get("phone")
    password = data.get("password")

    try:
        user = Account.objects.get(phone=phone)
    except Account.DoesNotExist:
        return Response({"message": "User does not exist"}, status=404)

    user.set_password(password)
    user.save()
    return Response({"login": True}, status=200)
class GetDashboardDataView(AdminView):

    def get(self, request):
        total_users = Account.objects.count()
        total_departmetns = Department.objects.count()
        attended = Attendance.objects.filter(status='p').count()
        not_attended = Attendance.objects.filter(status='a').count()
        data = {
            "total_users": total_users,
            "total_departments": total_departmetns,
            "present": attended,
            "absent": not_attended
        }
        
        return Response(data)
    



class UserDataView(AdminView):
    def get(self, request):
        users = Account.objects.all()
        data = []
        for user in users:
            attendance_records = Attendance.objects.filter(name=user,status='p').count()
            absent_records = Attendance.objects.filter(name=user,status='a').count()
            if user.department:
                data.append({
                    "id": user.id,
                    "name": user.__str__(),
                    "phone": user.phone,
                    "attended": attendance_records,
                    "absent": absent_records,
                    "department": user.department.name if user.department else None
                })
        return Response(data)
    
    def post(self, request):
        
        data = request.data
        department = Department.objects.get(id=data.get("department"))
        spiritual_title = SpiritualTitle.objects.get(id=data.get("spiritual_title")) if data.get("spiritual_title") else None
        secularity_title = SecularTitle.objects.get(id=data.get("secularity_title")) if data.get("secularity_title") else None
        
        user = Account.objects.create_user(
            phone=data.get("phone"),
            password=data.get("password"),
            name=data.get("name"),
            name_of_baptism=data.get("name_of_baptism","N/A"),
            department=department,
            spiritual_title=spiritual_title,
            secular_title=secularity_title
        )
        
        return Response({"message": "User creation endpoint - To be implemented","user": user.id}, status=201)

    

class DepartmentsView(AdminView):
    def get(self, request):
        departments = Department.objects.all()
        data = []
        for dept in departments:
            data.append({
                "id": dept.id,
                "name": dept.name,
            })
        return Response(data)
    
    def post(self, request):
        data = request.data
        existing_department = Department.objects.filter(name=data.get("name")).first()
        if existing_department:
            return Response({"message": "Department with this name already exists"}, status=400)
        department = Department.objects.create(name=data.get("name"))
        return Response({"message": "Department created successfully","department": department.id}, status=201)



class SpiritualTitlesView(AdminView):
    def get(self, request):
        departments = SpiritualTitle.objects.all()
        data = []
        for dept in departments:
            data.append({
                "id": dept.id,
                "name": dept.title,
            })
        return Response(data)

    
    def post(self, request):
        data = request.data
        existing_title = SpiritualTitle.objects.filter(title=data.get("name")).first()
        if existing_title:
            return Response({"message": "Spiritual title with this name already exists"}, status=400)
        title = SpiritualTitle.objects.create(title=data.get("name"))
        return Response({"message": "Spiritual title created successfully","spiritual_title": title.id}, status=201)
class SecularTitleView(AdminView):
    def get(self, request):
        departments = SecularTitle.objects.all()
        data = []
        for dept in departments:
            data.append({
                "id": dept.id,
                "name": dept.title,
            })
        return Response(data)
    

    def post(self, request):
        data = request.data
        existing_title = SecularTitle.objects.filter(title=data.get("name")).first()
        if existing_title:
            return Response({"message": "Secular title with this name already exists"}, status=400)
        title = SecularTitle.objects.create(title=data.get("name"))
        return Response({"message": "Secular title created successfully","secular_title": title.id}, status=201)