from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name="HMS-Home"),
    path('physicians/',views.physicians, name="Physicians"),
    path('surgeons/',views.surgeons, name="Surgeons"),
    path('nurses/',views.nurses, name="Nurses"),
    path('ward/',views.ward, name="Wards"),
]
