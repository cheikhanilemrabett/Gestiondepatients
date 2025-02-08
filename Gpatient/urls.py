# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('Admin_login/', views.Login, name='Admin_login'),
    path('Logout/', views.Logout_admin, name='Logout_admin'),
    path('index/', views.index, name='index'),
    path('view_doctor/', views.view_doctor, name='view_doctor'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_doctor/<int:pid>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:pid>/', views.delete_doctor, name='delete_doctor'),
    path('register/', views.register_patient, name='register_patient'),
    path('login/', views.login_patient, name='login_patient'),
    path('logout/', views.logout_patient, name='logout_patient'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('appointments/book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('complete-profile/', views.complete_patient_profile, name='complete_patient_profile'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('patients/', views.patients_list, name='patients_list'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('doctors/appointments/', views.appointments_list, name='appointments_list'),
  
    

]
   
    

   



