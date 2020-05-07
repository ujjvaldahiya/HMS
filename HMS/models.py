from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class physician(models.Model):
    physicianid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    dob = models.DateField(null=False)
    speciality = models.CharField(max_length=30,null=False)
    phoneno = models.BigIntegerField(unique=True, null=False)
    emailid = models.CharField(max_length=30, unique=True, null=False)
    occupied = models.BooleanField(null=False, default=False)

class nurse(models.Model):
    nurseid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    dob = models.DateField(null=False)
    phoneno = models.BigIntegerField(unique=True, null=False)
    emailid = models.CharField(max_length=30, unique=True, null=False)
    occupied = models.BooleanField(null=False, default=False)

class surgeon(models.Model):
    surgeonid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    dob = models.DateField(null=False)
    speciality = models.CharField(max_length=30,null=False)
    phoneno = models.BigIntegerField(unique=True, null=False)
    emailid = models.CharField(max_length=30, unique=True, null=False)
    occupied = models.BooleanField(null=False, default=False)

class ward(models.Model):
    wardid = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=20, null=False)
    type = models.CharField(max_length=30, null=False)
    occupied = models.BooleanField(null=False, default=False)

class patient(models.Model):
    patientid = models.AutoField(primary_key=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(null=False)
    date = models.DateField(null=False)
    treatmenttype = models.CharField(max_length=10, null=False)
    physicianid = models.ForeignKey(physician, on_delete=models.CASCADE, null=True, blank=True)
    surgeonid = models.ForeignKey(surgeon, on_delete=models.CASCADE, null=True, blank=True)
    regdate = models.DateField(default = timezone.now, null=False)
    paymentrefid = models.CharField(max_length=12, unique=True, null=False)

class prescription(models.Model):
    prescriptionid = models.AutoField(primary_key=True)
    patientid = models.ForeignKey(patient, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=False)
    treatment = models.TextField(null=False)
    medicine = models.TextField()

class report(models.Model):
    reportid = models.AutoField(primary_key=True)
    patientid = models.ForeignKey(patient, on_delete=models.CASCADE)
    tests = models.TextField(null=False)
    results = models.TextField(null=False)
