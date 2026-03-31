from attendance.models import Attendance
from datetime import date
from users.models import Account

def mark_attendance():
    users = Account.objects.all()
    today = date.today()

    for user in users:
        exists = Attendance.objects.filter(name=user, date=today).exists()
        
        if not exists:
            Attendance.objects.create(
                name=user,
                status='a'
            )