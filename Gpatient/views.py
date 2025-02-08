# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Department, Doctor, Patient, Appointment
from .forms import DoctorForm, PatientProfileForm, PatientSignUpForm
import csv

# General Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def index(request):
    if not request.user.is_staff:  
        return redirect('login')

    # حساب الإحصائيات
    total_patients = Patient.objects.count()  # حساب عدد المرضى
    total_doctors = Doctor.objects.count()  # حساب عدد الأطباء
    total_appointments = Appointment.objects.count()  # حساب عدد المواعيد

    return render(request, 'index.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments
    })






# Admin Authentication Views
def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', {'error': error})

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('home')

# Doctor Management Views

@login_required
def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.select_related('department').all()
    if not doctors:
        error_message = "No doctors found."
        return render(request, 'doctors/view_doctor.html', {'error_message': error_message})
    return render(request, 'doctors/view_doctor.html', {'doctors': doctors})


@login_required
def delete_doctor(request, pid):
    if not request.user.is_staff:
        messages.error(request, "You must be an admin to perform this action.")
        return redirect('veiw_doctor')
    doctor = get_object_or_404(Doctor, pk=pid)
    doctor.delete()
    messages.success(request, f"Doctor {doctor.Name} deleted successfully!")
    return redirect('view_doctor')

@login_required
def add_doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        n = request.POST['name']
        add = request.POST['address']
        spe_id = request.POST['specialiste']
        age = request.POST['age']
        try:
            department = Department.objects.get(DepId=spe_id)
            Doctor.objects.create(Name=n, address=add, age=age, department=department)
            error = "no"
        except Department.DoesNotExist:
            error = "invalid_department"
        except Exception:
            error = "yes"
    departments = Department.objects.all()
    return render(request, 'doctors/add_doctor.html', {'error': error, 'departments': departments})

@login_required
def edit_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = get_object_or_404(Doctor, pk=pid)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doctor {doctor.Name} has been updated successfully!")
            return redirect('view_doctor')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/edit_doctor.html', {'form': form, 'doctor': doctor})

# Patient Authentication and Profile Views
def register_patient(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'patients/register.html', {'form': form})

def login_patient(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'patients/login.html', {'form': form})

def logout_patient(request):
    logout(request)
    return redirect('login_patient')

@login_required
def complete_patient_profile(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        if request.method == "POST":
            form = PatientProfileForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = request.user
                patient.save()
                return redirect('patient_dashboard')
        else:
            form = PatientProfileForm()
        return render(request, 'patients/complete_profile.html', {'form': form})

# Appointment Management Views
@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "You need to complete your patient profile.")
        return redirect('complete_patient_profile')
    query = request.GET.get('search', '')
    doctors = Doctor.objects.filter(Name__icontains=query) if query else Doctor.objects.all()
    appointments = Appointment.objects.filter(patient=patient)
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor = Doctor.objects.get(id=doctor_id)
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            messages.error(request, "This time slot is already booked. Please select a different time.")
        else:
            Appointment.objects.create(patient=patient, doctor=doctor, date=date, time=time)
            messages.success(request, "Appointment booked successfully!")
    return render(request, 'patients/dashboard.html', {
        'doctors': doctors,
        'appointments': appointments,
        'query': query
    })

@login_required
def doctors_list(request):
    query = request.GET.get('search', '')
    doctors = Doctor.objects.filter(Name__icontains=query) if query else Doctor.objects.all()
    return render(request, 'patients/doctors_list.html', {'doctors': doctors, 'query': query})

@login_required
def book_appointment(request, doctor_id):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor = Doctor.objects.get(id=doctor_id)
        patient = request.user.patient
        Appointment.objects.create(date=date, time=time, doctor=doctor, patient=patient)
        messages.success(request, "Appointment booked successfully!")
        return redirect('appointments_list')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'patients/book_appointment.html', {'doctor': doctor})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    appointment.delete()
    messages.success(request, "Appointment canceled successfully!")
    return redirect('patient_dashboard')

# Admin Patient and Appointment Management
@staff_member_required
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'doctors/patients_list.html', {'patients': patients})

@staff_member_required
def add_patient(request):
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        age = request.POST['age']
        phone = request.POST['phone']
        diseases_case = request.POST['diseases_case']
        gender = request.POST['gender']
        Patient.objects.create(
            Name=name,
            address=address,
            age=age,
            phone=phone,
            diseases_case=diseases_case,
            gender=gender
        )
        return redirect('patients_list')
    return render(request, 'admin/add_patient.html')

@staff_member_required
def delete_patient(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        if patient.user:
            patient.user.delete()
        patient.delete()
        messages.success(request, f"Patient {patient.Name} deleted successfully!")
    except Patient.DoesNotExist:
        pass
    return redirect('patients_list')

@staff_member_required
def appointments_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/appointments_list.html', {'appointments': appointments})

def export_csv(request):
    patients = Patient.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Phone'])
    for patient in patients:
        writer.writerow([patient.Name, patient.age, patient.phone])
    return response

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def appointments_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    return render(request, '/appointments_list.html', {'appointments': appointments})





