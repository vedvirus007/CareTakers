from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, NewInvoice, billGenerator, createUser, generated, getDoctors, handlelogout, invoice,make_appoint, make_predict, userlogin

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", make_appoint, name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
    path("make-prediction/", make_predict, name="prediction"),
    path("user/", createUser, name="user"),
    path('userlogin/', userlogin),
     path('logout/', handlelogout),
    path('generator/', billGenerator),
    path('generated/', generated),
    path('patients/<int:id>/invoice/', invoice),
    path('NewInvoice/', NewInvoice),
    path('doctors/', getDoctors),

]
