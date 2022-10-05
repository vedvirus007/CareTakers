from django.db import models
from django.http import request

class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    clinic_name = models.TextField(blank=False)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]

class clinic(models.Model):
    clinic_name=models.CharField(max_length=25)
    doctor_name=models.CharField(max_length=25)
    qualification=models.CharField(max_length=50)
    # hospital_name=models.TextField()
    # host_email=models.CharField(max_length=40)
    # host_phone=models.CharField(max_length=15)
    # host_pass=models.CharField(max_length=20)
    def __str__(self):
       return self.clinic_name 

class Prediction(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    output = models.TextField(blank=True)
    def __str__(self):
       return self.first_name 

class patient(models.Model):

    patient_name=models.CharField(max_length=25)
    status=models.CharField(max_length=50)
    illness=models.TextField(null=True,blank=True)
    doctor_select=models.TextField(default='Vivek')
    hos_name=models.CharField(max_length=50, blank=True, null=True)
    cost=models.IntegerField(null=True,blank=True)  
    med_cost=models.IntegerField(null=True,blank=True)
    discount_cost=models.IntegerField(null=True,blank=True)
    total_cost=models.IntegerField(null=True,blank=True)
    blood_test=models.BooleanField(null=True,blank=True)
    general_checkup=models.BooleanField(null=True,blank=True)
    chest_xray=models.BooleanField(null=True,blank=True)
    ct_scan=models.BooleanField(null=True,blank=True)
    dental_treatment=models.BooleanField(null=True,blank=True)
    ET_Treatment=models.BooleanField(null=True,blank=True)
    Full_checkup=models.BooleanField(null=True,blank=True)
    # host_email=models.CharField(max_length=40)
    # host_phone=models.CharField(max_length=15)
    # host_pass=models.CharField(max_length=20)
    def __str__(self):
       return self.patient_name
        