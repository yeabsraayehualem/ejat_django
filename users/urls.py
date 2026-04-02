from django.urls import path
from . import views



urlpatterns = [
    path("api/init/", views.check_user),
    path("api/set-password/", views.set_password),
    path('api/login/', views.JWTAuthCustom.as_view(), name='token_obtain_pair'),
    path('api/admin/dashboard/', views.GetDashboardDataView.as_view(), name='dashboard_data'),
    path('api/admin/users/', views.UserDataView.as_view(), name='user_data'),
    path("api/admin/departments/", views.DepartmentsView.as_view(), name='departments_data'),
    path("api/admin/spiritual-titles/", views.SpiritualTitlesView.as_view(), name='spiritual_titles_data'),
    path("api/admin/secular-titles/", views.SecularTitleView.as_view(), name='secular_titles_data'),

]