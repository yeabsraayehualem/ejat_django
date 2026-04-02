from django.views import View

from attendance.models import Attendance
from datetime import date
from users.models import Account, Department


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



import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm
import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CSVUploadForm
@login_required
def upload_csv(request):
    data = []

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            existing_phones = set(Account.objects.values_list('phone', flat=True))
            dept_cache = {}
            new_users = []

            for row in reader:
                if row == ['ስም', 'ስልክ ቁጥር', 'የአገልግሎት ቤተሰብ', 'የክርስትና ስም']:
                    continue
                if row == ['', '', '', '']:
                    break
                if row[1] == '' or row[1] in existing_phones:
                    continue

                # Department caching
                dept_name = row[2]
                if dept_name in dept_cache:
                    dept = dept_cache[dept_name]
                else:
                    dept, _ = Department.objects.get_or_create(name=dept_name)
                    dept_cache[dept_name] = dept

                # create user object
                user = Account(
                    name=row[0],
                    phone=row[1],
                    department=dept,
                )
                user.set_password(row[1])
                new_users.append(user)
                existing_phones.add(row[1])

                data.append(row)

            # Bulk insert all users at once
            Account.objects.bulk_create(new_users)

    else:
        form = CSVUploadForm()

    return render(request, 'upload.html', {
        'form': form,
        'data': data
    })