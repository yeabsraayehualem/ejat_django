from django.contrib import admin
from .models import Department,SecularTitle,SpiritualTitle,Account


admin.site.register(Department)
admin.site.register(SpiritualTitle)
admin.site.register(SecularTitle)
admin.site.register(Account)
