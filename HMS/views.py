from django.shortcuts import render, HttpResponse
from HMS import models

# Create your views here.

def home(request):
    return render(request, 'HMS/hms.html')

def physicians(request):
    if request.method == "POST":
        filter = request.POST['speciality']
        if filter != 'All specialities':
            physicians = models.physician.objects.filter(speciality=request.POST['speciality']).order_by('physicianid')
        else:
            physicians = models.physician.objects.all().order_by('physicianid')
    else:
        physicians = models.physician.objects.all().order_by('physicianid')
        filter = 'None'
    specialities = models.physician.objects.all().distinct('speciality').values_list('speciality', flat=True)
    return render(request, 'HMS/physicians.html', {'specialities': specialities, 'physicians': physicians, 'filter':filter})

def surgeons(request):
    if request.method == "POST":
        filter = request.POST['speciality']
        if filter != 'All specialities':
            surgeons = models.surgeon.objects.filter(speciality=request.POST['speciality']).order_by('surgeonid')
        else:
            surgeons = models.surgeon.objects.all().order_by('surgeonid')
    else:
        surgeons = models.surgeon.objects.all().order_by('surgeonid')
        filter = 'None'
    specialities = models.surgeon.objects.all().distinct('speciality').values_list('speciality', flat=True)
    return render(request, 'HMS/surgeons.html', {'specialities': specialities, 'surgeons': surgeons, 'filter':filter})

def nurses(request):
    nurses = models.nurse.objects.all().order_by('nurseid')
    return render(request, 'HMS/nurses.html', {'nurses':nurses})

def ward(request):
    if request.method == "POST":
        filterT = request.POST['type']
        filterG = request.POST['gender']
        if filterT != 'All Types' and filterG != 'All Genders':
            wards = models.ward.objects.filter(type=filterT, gender=filterG).order_by('wardid')
        elif filterT != 'All Types' and filterG == 'All Genders':
            wards = models.ward.objects.filter(type=filterT).order_by('wardid')
        elif filterT == 'All Types' and filterG != 'All Genders':
            wards = models.ward.objects.filter(gender=filterG).order_by('wardid')
        else:
            wards = models.ward.objects.all().order_by('wardid')
    else:
        wards = models.ward.objects.all().order_by('wardid')
        filterT = 'None'
        filterG = 'None'
    types = models.ward.objects.all().distinct('type').values_list('type', flat=True)
    genders = models.ward.objects.all().distinct('gender').values_list('gender', flat=True)
    return render(request, 'HMS/ward.html', {'types': types, 'genders':genders ,'wards': wards, 'filterT':filterT, 'filterG':filterG})

#def report(request):

#def bill(request):

#def appointment(request):
