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

            for row in reader:

                if row == ['ስም', 'ስልክ ቁጥር', 'የአገልግሎት ቤተሰብ', 'የክርስትና ስም']:
                    continue

                if row == ['', '', '', '']:
                    break

                if row[1] == '':
                    continue

                dept, _ = Department.objects.get_or_create(name=row[2])
                ex = Account.objects.filter(phone=row[1]).filter()
                if ex:
                    continue

                user, created = Account.objects.get_or_create(
                    name=row[0],
                    phone=row[1],
                    department=dept
                )

                user.set_password(row[1])
                user.save()

                data.append(row)

    else:
        form = CSVUploadForm()

    return render(request, 'upload.html', {
        'form': form,
        'data': data
    })