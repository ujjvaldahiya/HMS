from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from users import models
from HMS import models as hms_models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from users.appointment import Appointment
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login.')
            return redirect('Login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def change_password(request):
    utype = models.Profile.objects.get(user = request.user).usertype
    if request.method == 'POST':
        obj = User.objects.get(username__exact=request.user.username)
        if obj.check_password(request.POST['oldpassword']):
            if request.POST['newpassword'] == request.POST['cpassword']:
                obj.set_password(request.POST['newpassword'])
                obj.save()
                error = 'Password Changed Successfully!'
            else:
                error = 'New Password and Confirm Password fields do not match!'
        else:
            error = 'Incorrect Old Password!'
    else:
        error = 'None'

    return render(request, 'users/change_password.html', {'error': error, 'utype': utype})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'utype': models.Profile.objects.get(user = request.user).usertype
    }

    return render(request, 'users/profile.html', context)

################################################################################

@login_required
def view_prescriptions(request, prescriptionid):
    utype = models.Profile.objects.get(user = request.user).usertype
    prescriptions = hms_models.prescription.objects.filter(patientid__user__username = request.user.username).values_list('prescriptionid', flat=True)

    if utype == 'laboratory' or (utype == 'patient' and not(prescriptionid in prescriptions)):
        return render(request, 'users/unauthorised.html')

    if utype == 'surgeon' or 'physician':
        try:
            prescription = hms_models.prescription.objects.get(patientid = prescriptionid)
            error= 'None'
        except:
            prescription = 'None'
            error = 'Your physician/surgeon has not yet filled the prescription. Try again later.'
    else:
        prescription = hms_models.prescription.objects.get(prescriptionid = prescriptionid)
        error = 'None'

    return render(request, 'users/view_prescription.html', {'prescription':prescription, 'error':error, 'utype':utype})

@login_required
def prescriptions(request):
    utype = models.Profile.objects.get(user = request.user).usertype
    if not(utype in ['medicalstore', 'patient']):
        return render(request, 'users/unauthorised.html')

    if utype == 'patient':
        prescriptions = hms_models.prescription.objects.filter(patientid__user__username=request.user.username)
    else:
        prescriptions = hms_models.prescription.objects.filter(patientid__date=datetime.now())

    return render(request, 'users/prescriptions.html', {'prescriptions': prescriptions, 'utype': utype, 'error': 'None'})

@login_required
def new_prescription(request, patientid):
    utype = models.Profile.objects.get(user = request.user).usertype

    if not(utype in ['surgeon', 'physician'] ):
        return render(request, 'users/unauthorised.html')

    error = 'None'
    patient = hms_models.patient.objects.get(patientid=patientid)
    if request.method == 'POST':
        try:
            obj = hms_models.prescription(
                                            patientid = patient,
                                            diagnosis = request.POST['diagnosis'],
                                            treatment = request.POST['treatment'],
                                            medicine = request.POST['medicine']
                                            )
            obj.save()
            error = 'Submission Successful'
        except:
            error = 'Something Wrong Happened! Try again.'

    return render(request, 'users/new_prescription.html', {'patient':patient, 'error': error, 'utype': utype})


################################################################################

@login_required
def lab_reports(request):
    utype = models.Profile.objects.get(user = request.user).usertype
    if not(utype in ['laboratory', 'patient']):
        return render(request, 'users/unauthorised.html')

    if utype == 'patient':
        reports = hms_models.report.objects.filter(patientid__user__username=request.user.username)
    else:
        reports = hms_models.report.objects.filter(patientid__date=datetime.now())

    return render(request, 'users/lab_reports.html', {'reports': reports, 'utype': utype, 'error': 'None'})

@login_required
def view_labreport(request, reportid):
    utype = models.Profile.objects.get(user = request.user).usertype
    reports = hms_models.report.objects.filter(patientid__user__username = request.user.username).values_list('reportid', flat=True)

    if utype == 'medicalstore' or (utype == 'patient' and not(reportid in reports)):
        return render(request, 'users/unauthorised.html')


    if utype == 'physician' or utype == 'surgeon':
        try:
            report = hms_models.report.objects.get(patientid = reportid)
            error = 'None'
        except:
            report = 'None'
            error = 'Your physician/surgeon has not yet filled the report. Try again later.'
    else:
        report = hms_models.report.objects.get(reportid = reportid)
        error = 'None'

    return render(request, 'users/view_labreport.html', {'report':report, 'error':error, 'utype':utype})

@login_required
def new_labtest(request, patientid):
    utype = models.Profile.objects.get(user = request.user).usertype

    if not(utype in ['surgeon', 'physician'] ):
        return render(request, 'users/unauthorised.html')

    error = 'None'
    patient = hms_models.patient.objects.get(patientid=patientid)
    if request.method == 'POST':
        try:
            obj = hms_models.report(
                                    patientid = patient,
                                    tests = request.POST['tests'],
                                    results = '---to be filled---'
                                    )
            obj.save()
            error = 'Submission Successful'
        except:
            error = 'Something Wrong Happened! Try again.'

    return render(request, 'users/new_labtest.html', {'patient':patient, 'error': error, 'utype': utype})

@login_required
def result_labtest(request, patientid):
    utype = models.Profile.objects.get(user = request.user).usertype

    if utype != 'laboratory':
        return render(request, 'users/unauthorised.html')

    error = 'None'
    patient = hms_models.patient.objects.get(patientid=patientid)
    obj = hms_models.report.objects.get(patientid = patient)
    if request.method == 'POST':
        try:
            obj.results = request.POST['result']
            obj.save()
            error = 'Submission Successful'
        except:
            error = 'Something Wrong Happened! Try again.'

    return render(request, 'users/result_labtest.html', {'patient':patient, 'error': error, 'test': obj, 'utype':utype})

###############################################################################

@login_required
def appointments(request):
    utype = models.Profile.objects.get(user = request.user).usertype

    if utype in ['laboratory','medicalstore']:
        return render(request, 'users/unauthorised.html')

    appointments = []
    if utype == 'patient':
        appointments = hms_models.patient.objects.filter(user__username=request.user.username)
    elif request.method == 'POST':
        if utype == 'surgeon':
            appointments = hms_models.patient.objects.filter(date=datetime.now(), surgeonid = request.POST['id'])
        else:
            appointments = hms_models.patient.objects.filter(date=datetime.now(), physicianid = request.POST['id'])

    return render(request, 'users/appointments.html', {'appointments': appointments, 'utype':utype, 'error': 'None'})

@login_required
def new_appointment(request):
    keys = ['sdate', 'sttype', 'sspeciality', 'sdoctor', 'stime']
    apt = Appointment()
    args = apt.resetForm()

    if request.method == 'POST':
        ######### get previous state ################
        if request.session.has_key('pstate'):
            change = None
            pstate = request.session['pstate']
            for key in keys[0:4]:
                if pstate[key] != request.POST[key[1:]]:
                    change = key
                    break
            pstate = {
                        'sdate' : request.POST['date'],
                        'sttype' : request.POST['ttype'],
                        'sspeciality': request.POST['speciality'],
                        'sdoctor': request.POST['doctor'],
                        'stime': request.POST['time']
                        }
        else:
            pstate = None
            change = None

        ################################################
        if pstate == None or change == 'sdate':
            args['sdate'] = request.POST['date']
            request.session['pstate'] = pstate
        elif change == 'sttype':
            args['sdate'] = request.POST['date']
            args['sttype'] = request.POST['ttype']
            args['specialities'] = apt.getSpecialities(request.POST['ttype'])
            request.session['pstate'] = pstate
        elif change == 'sspeciality':
            args['sdate'] = request.POST['date']
            args['sttype'] = request.POST['ttype']
            args['specialities'] = apt.getSpecialities(request.POST['ttype'])
            args['sspeciality'] = request.POST['speciality']
            args['doctors'] = apt.getDoctors(request.POST['ttype'], request.POST['speciality'])
            request.session['pstate'] = pstate
        elif change == 'sdoctor':
            args['sdate'] = request.POST['date']
            args['sttype'] = request.POST['ttype']
            args['specialities'] = apt.getSpecialities(request.POST['ttype'])
            args['sspeciality'] = request.POST['speciality']
            args['doctors'] = apt.getDoctors(request.POST['ttype'], request.POST['speciality'])
            args['sdoctor'] = request.POST['doctor']
            args['times'] = apt.getTimes(request.POST['ttype'], request.POST['doctor'], request.POST['date'])
            request.session['pstate'] = pstate
        else:
            message = apt.appoint(
                        request.user,
                        request.POST['date'],
                        request.POST['ttype'],
                        request.POST['speciality'],
                        request.POST['doctor'],
                        request.POST['time'])
            args = apt.resetForm()
            args['error'] = message[1]
            if message[0]:
                request.session['pstate'] = {
                        'sdate' : '-------',
                        'sttype' : '-------',
                        'sspeciality': '-------',
                        'sdoctor': '-------',
                        'stime': '-------'
                        }
    else:
        request.session['pstate'] = {
                'sdate' : '-------',
                'sttype' : '-------',
                'sspeciality': '-------',
                'sdoctor': '-------',
                'stime': '-------'
                }

    return render(request, 'users/new_appointment.html', args)

@login_required
def view_appointment(request, patientid):
    utype = models.Profile.objects.get(user = request.user).usertype
    error = 'None'
    try:
        patient = hms_models.patient.objects.get(patientid=patientid)
        if patient.user.username != request.user.username:
            return render(request, 'users/unauthorised.html')
        error = 'None'
    except:
        return render(request, 'users/unauthorised.html')

    return render(request, 'users/view_appointment.html', {'patient':patient, 'error':error, 'utype':utype})

################################################################################

@login_required
def book_nurse(request):
    utype = models.Profile.objects.get(user = request.user).usertype
    error = 'None'

    if not(utype in ['surgeon', 'physician'] ):
        return render(request, 'users/unauthorised.html')

    try:
        nurses = hms_models.nurse.objects.filter(occupied=False)
        if nurses:
            nurse = hms_models.nurse.objects.get(nurseid = nurses[0].nurseid)
            nurse.occupied = True
            nurse.save()
            error = 'Nurse %s id: %s appointed.'%(nurse.name, nurse.nurseid)
        else:
            error = 'No nurse available at the moment. Try again later.'
    except:
        error='Something Wrong Happened! Try again'
    return render(request, 'users/appointments.html', {'appointments':appointments, 'utype':utype, 'error':error})

@login_required
def book_ward(request, patientid):
    utype = models.Profile.objects.get(user = request.user).usertype

    if not(utype in ['surgeon', 'physician'] ):
        return render(request, 'users/unauthorised.html')

    error = 'None'
    patient = hms_models.patient.objects.get(patientid=patientid)

    genders = ['-------'] + list(hms_models.ward.objects.filter(occupied=False).distinct('gender').values_list('gender', flat=True))
    if request.method == 'POST':
        sgender = request.POST['gender']
        stype = request.POST['type']

        if sgender != '-------':
            types = ['-------'] + list(hms_models.ward.objects.filter(occupied=False, gender=sgender).distinct('type').values_list('type', flat=True))

        if sgender != '-------' and stype != '-------':
            obj = hms_models.ward.objects.filter(occupied=False, type=stype, gender=sgender)
            if obj:
                try:
                    ward = hms_models.ward.objects.get(wardid=obj[0].wardid)
                    ward.occupied = True
                    ward.save()
                    error = 'Ward booked Successfully!'
                except:
                    error = 'Something Wrong Happened! Try again.'
                    types = ['-------']
                    sgender = '-------'
                    stype = '-------'
            else:
                error = 'Ward not available!'
                types = ['-------']
                sgender = '-------'
                stype = '-------'

    else:
        types = ['-------']
        sgender = '-------'
        stype = '-------'

    return render(request, 'users/book_ward.html', { 'utype': utype, 'patient': patient ,'error':error, 'genders': genders, 'types': types, 'sgender': sgender, 'stype': stype})
