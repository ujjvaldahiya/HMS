"""hospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('profile/', users_views.profile, name='Profile'),
    path('register/', users_views.register, name='Register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='Logout'),
    path('change-password/',users_views.change_password, name="Change_Password"),

    path('prescriptions/',users_views.prescriptions, name="Prescriptions"),
    path('prescriptions/<int:prescriptionid>',users_views.view_prescriptions, name="View_Prescriptions"),
    path('prescriptions/new/<int:patientid>',users_views.new_prescription, name="New_Prescription"),

    path('appointments/',users_views.appointments, name="Appointments"),
    path('appointments/<int:patientid>',users_views.view_appointment, name="View_Appointment"),
    path('appointments/new',users_views.new_appointment, name="New_Appointment"),

    path('lab_reports/',users_views.lab_reports, name="Lab_Reports"),
    path('lab_reports/<int:reportid>',users_views.view_labreport, name="View_LabReport"),
    path('lab_reports/edit/result/<int:patientid>',users_views.result_labtest, name="Result_LabTest"),
    path('lab_reports/edit/<int:patientid>',users_views.new_labtest, name="New_LabTest"),

    path('nurse/appoint',users_views.book_nurse, name="Book_Nurse"),
    path('ward/book/<int:patientid>',users_views.book_ward, name="Book_Ward"),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('HMS.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
