from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.GetAttendancesView.as_view(), name='attendance'),
]