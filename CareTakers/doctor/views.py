from statistics import mode
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment,clinic,Prediction, patient
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
import pandas as pd
import numpy as np
import joblib
m={'Paroymsal Positional Vertigo' : 'Physiotherapist',
'AIDS': 'Infectious Disease Doctor',
'Acne' : 'Dermatologist',
'Alcoholic hepatitis':'Hepatologist',
'Allergy': 'Allergist',
'Arthritis':'rheumatologist',
'Bronchial Asthma':'Pulmonologist',
'Cervical spondylosis':'Orthopedist',
'Chicken pox': 'Infectitious Doctor',
'Chronic cholestasis':'Gastroenterology', 
'Common Cold':'Physician',
'Dengue':'Infectitious Doctor',
'Diabetes':'endocrinologist',
'Dimorphic hemmorhoids(piles)':'General Physician',
'Drug Reaction':'Allergist',
'Fungal infection': 'Dermatologist',
'GERD':'Gastroenterologist',
'Gastroenteritis':'Gastroenterologist',
'Heart attack':'Cardiologist',
'Hepatitis B':'Hepatologist',
'Hepatitis E':'Hepatologist',
'Hypertension':'Nephrologist',
'Hyperthyroidism':'Endocrinologist',
'Hypoglycemia':'Endrocrinologist',
'Impetigo':'Dermatologist',
'Jaundice':'Gastroenterologist',
'Malaria':'General Physician',
'Migraine':'Neurologist',
'Osteoarthristis':'Rheumatologist',
'Paralysis' :'Neurologist',
'Peptic ulcer diseae':'Gastroenterologist',
'Pneumonia':'Pulmonologist',
'Psoriasis':'Rheumatologist',
'Tuberculosis':'Pulmonologist',
'Typhoid':'Infectitious Disease Doctor',
'Urinary tract infection':'Gynecologist',
'Varicose veins':'Dermatologist',
'hepatitis A':'Gastroenterologist'}

class HomeTemplateView(TemplateView):
    template_name = "index.html"
    
    # def post(self, request):
    #     name = request.POST.get("name")
        # email = request.POST.get("email")
        # message = request.POST.get("message")

        # email = EmailMessage(
        #     subject= f"{name} from doctor family.",
        #     body=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     to=[settings.EMAIL_HOST_USER],
        #     reply_to=[email]
        # )
        # email.send()
        # return HttpResponse("Email sent successfully!")

def make_appoint(request):
    context={'clinics':clinic.objects.all()}
    if request.method=="POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        doctor_select=request.POST.get("select_doctor")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")
        context={'clinics':clinic.objects.all()}
        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
            clinic_name=doctor_select,
        )
        appointment.save()
        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        # return HttpResponseRedirect(request.path)
    return render(request, 'appointment.html',context)


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"
    context={'clinics':clinic.objects.all()}
    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        doctor_select=request.POST.get("select_doctor")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")
        # context={'clinics':clinic.objects.all()}

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
            clinic_name=doctor_select,
        )

        appointment.save()
        # context={'clinics':clinic.objects.all()}

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        # return HttpResponseRedirect(request.path)
        return render(request, 'appointment.html',{'clinics':clinic.objects.all()})

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3


    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        # message = get_template('email.html').render(data)
        # email = EmailMessage(
        #     "About your appointment",
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [appointment.email],
        # )
        # email.content_subtype = "html"
        # email.send()

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)


    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context



# Defining the Function
# Input: string containing symptoms separated by commmas
# Output: Generated predictions by models
def predictDisease(symptoms):
    DATA_PATH = "Prediction/dataset/Training.csv"
    data = pd.read_csv(DATA_PATH).dropna(axis = 1)
    X = data.iloc[:,:-1]
    symptoms1= X.columns.values
    symptom_index = {}
    for index, value in enumerate(symptoms1):
        symptom = " ".join([i.capitalize() for i in value.split("_")])
        symptom_index[symptom] = index
    encoder = LabelEncoder()
    data["prognosis"] = encoder.fit_transform(data["prognosis"])
    data_dict = {
        "symptom_index":symptom_index,
        "predictions_classes":encoder.classes_
    }
    # creating input data for the models
    # symptoms = symptoms.split(",")

    input_data = [0] * len(data_dict["symptom_index"])
    # print(symptoms)
    # print("yes")
    symptoms = symptoms.split(",")
    for symptom in symptoms:
        
        index = data_dict["symptom_index"][symptom]
        # print(index)
        input_data[index] = 1
        
    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)
    final_rf_model=joblib.load('Prediction/rf_model.sav')
    final_nb_model=joblib.load('Prediction/nb_model.sav')
    final_svm_model=joblib.load('Prediction/svm_model.sav')
    

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
    predictions = {
		"rf_model_prediction": rf_prediction,
		"naive_bayes_prediction": nb_prediction,
		"svm_model_prediction": nb_prediction,
		# "final_prediction":final_prediction
	}
    s=max(predictions["rf_model_prediction"],predictions["naive_bayes_prediction"],predictions["svm_model_prediction"])
    return s

def make_predict(request):
    context={'pred':"NO disease"}
    if request.method=="POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        # doctor_select=request.POST.get("select_doctor")
        mobile = request.POST.get("mobile")
        symptoms = request.POST.get("request")
        l=len(symptoms)
        symptoms=symptoms[:l-1]
        
        print(symptoms)
        output=predictDisease(symptoms)
        print(output)
        print(type(output))
        # context={'clinics':clinic.objects.all()}
        appointment = Prediction.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=symptoms,
            output=output,
            # clinic_name=doctor_select,
        )
        appointment.save()
        # context={'pred':output}
        
        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for taking predictions, Your prediction are "+output+". We recoomend you to visit  " +m[output] + ".")
        # print(output)
        return HttpResponseRedirect(request.path)
    return render(request, 'predict.html',context)

def createUser(request):
    if request.method=='POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        print(fname)
        # doctor_select=request.POST.get("select_doctor")
        password = request.POST.get("mobile")
        # symptoms = request.POST.get("request")
        user = User.objects.create_user(username=fname, email=email,password=password)
        user.save()
        ins=patient(patient_name=fname)
        ins.save()
    return render(request,'user.html')

def userlogin(request):
    
    if request.method=="POST":
        loginusername=request.POST.get('loginusername')
        pass1=request.POST.get('pass1')
        user=authenticate(username=loginusername,password=pass1)
        
        if user is not None:
            login(request,user)
            
    return render(request, 'login.html')

def handlelogout(request):
    logout(request)
    return render(request, 'logout_user.html') 


def billGenerator(request):
   
    return render(request, 'invoice_generator.html')
def invoice(request,id):
    pat_obj = patient.objects.get(id=id)
    context = {
        'pat' : pat_obj
    }
    return render(request, 'invoice.html',context)       
def generated(request):
    if request.method=="POST":
        f_name = request.POST['name']
        h_name = request.POST['hospitalname']
        med_cost = request.POST['medicine']
        blood = request.POST.get('blood',False)
        general = request.POST.get('general',False)
        xray = request.POST.get('xray',False)
        ct = request.POST.get('ct',False)
        dental = request.POST.get('dental',False)
        et = request.POST.get('et',False)
        full = request.POST.get('full',False)
        # checks = request.POST.getlist('checks[]')
        # print(checks)
        # cost = 0
        # for i in checks:
        #     cost+=int(i)*500
        # cost+=int(med_cost)  
        m = int(med_cost)  
        cost=0
        if blood=="True":
            cost = cost + int(500)
        if general=="True":
            cost += int(1000)
        if xray=="True":
            cost = cost + 1500
        if ct=="True":
            cost += 2000
        if dental=="True":
            cost += 2500
        if et=="True":
            cost += 3000
        if full=="True":
            cost = cost+ 3500   
        cost += m  
        print(cost)
        discount_cost = 0.1*int(cost)
        total_cost = 0.9*int(cost)  
        pat = patient.objects.get(patient_name=f_name)            
        ins = patient(hos_name = h_name, cost = cost,med_cost=med_cost,discount_cost=discount_cost,total_cost=total_cost,blood_test=blood,general_checkup=general,chest_xray=xray,ct_scan=ct,dental_treatment=dental,ET_Treatment=et,Full_checkup=full)   
        pat.hos_name=h_name
        pat.cost=cost

        pat.med_cost=med_cost
        pat.discount_cost=discount_cost
        pat.total_cost=total_cost
        pat.blood_test=blood
        pat.general_checkup=general
        pat.chest_xray=xray
        pat.ct_scan=ct
        pat.dental_treatment=dental
        pat.ET_Treatment=et
        pat.Full_checkup=full
        pat.save()
        context={'name':f_name}
        print(cost, f_name, h_name)
    return render(request, 'generated.html',context)

def NewInvoice(request):
    if request.method=="POST":
        return render(request, 'new_invoice.html') 
def getDoctors(request):
    return render(request, 'index1.html') 