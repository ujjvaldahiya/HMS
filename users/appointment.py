from users import models
from HMS import models as hms_models
from datetime import datetime, timedelta
import random, string

def randomword(length):
   letters = string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

class Appointment:

    def __init__(self):
        self.times = ['-------']
        for i in range(9,17):
            for j in range(0,60,15):
                if i == 9:
                    h = '09'
                else:
                    h = i
                if j == 0:
                    m = '00'
                else:
                    m = j
                self.times.append('%s:%s'%(h,m))

    def getDates(self):
        dates = ['-------']
        date = datetime.now()
        for _ in range(7):
            dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=1)
        return dates

    def getSpecialities(self, sttype):
        specialities = ['-------']
        if sttype == 'surgery':
            specialities = specialities + list(hms_models.surgeon.objects.all().distinct('speciality').values_list('speciality', flat=True))
        else:
            specialities = specialities + list(hms_models.physician.objects.all().distinct('speciality').values_list('speciality', flat=True))

        return specialities

    def getDoctors(self, sttype, sspeciality):
        doctors = ['-------']
        if sttype == 'surgery':
            doctors = doctors + list(hms_models.surgeon.objects.filter(speciality=sspeciality).values('surgeonid','name'))
        else:
            doctors = doctors + list(hms_models.physician.objects.filter(speciality=sspeciality).values('physicianid','name'))

        for i in range(1,len(doctors)):
            if sttype == 'surgery':
                doctors[i] = '(' + str(doctors[i]['surgeonid']) + ')' + doctors[i]['name']
            else:
                doctors[i] = '(' + str(doctors[i]['physicianid']) + ')' + doctors[i]['name']

        return doctors

    def getTimes(self, sttype, sdoctor, sdate):
        times = self.times
        if sttype == 'surgery':
            times = ['-------', '09:00']
            ttimes =  list(hms_models.patient.objects.filter(
                            date=sdate,
                            surgeonid = int(sdoctor.split(')')[0][1:])
                            ).values_list('time', flat=True))

        else:
            ttimes =  list(hms_models.patient.objects.filter(
                            date=sdate,
                            physicianid = int(sdoctor.split(')')[0][1:])
                            ).values_list('time', flat=True))
        for x in ttimes:
            try:
                times.remove(x.strftime('%H:%M'))
            except:
                pass
        return times

    def appoint(self, user, sdate, sttype, sspeciality, sdoctor, stime):
        try:
            obj = hms_models.patient(
                        user=user,
                        date = sdate,
                        treatmenttype = sttype,
                        paymentrefid = randomword(12),
                        time = stime
                        )
            if sttype == 'surgery':
                obj.surgeonid = hms_models.surgeon.objects.get(surgeonid=int(sdoctor.split(')')[0][1:]))
            else:
                obj.physicianid = hms_models.physician.objects.get(physicianid=int(sdoctor.split(')')[0][1:]))

            obj.save()
        except:
            return (False, 'some error occured!')
        return (True, 'Appointment Successful!')

    def resetForm(self):
        parms = {
                    'error' : 'None',
                    'dates' : self.getDates(),
                    'sdate' : '-------',
                    'ttypes' : ['-------', 'checkup', 'surgery'],
                    'sttype' : '-------',
                    'specialities' : ['-------'],
                    'sspeciality' : '-------',
                    'doctors' : ['-------'],
                    'sdoctor' : '-------',
                    'times' : ['-------'],
                    'stime' : '-------',
                }
        return parms
