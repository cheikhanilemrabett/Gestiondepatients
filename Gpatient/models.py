from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    DepId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    def __str__(self): 
        return self.name


class Doctor(models.Model):
    Name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    
    def __str__(self): 
        return self.Name


from django.contrib.auth.hashers import make_password, check_password

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    phone = models.CharField(max_length=200, unique=True)
    diseases_case = models.IntegerField()
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    def __str__(self): 
        return self.Name


    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
       
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_appointments')
    
    class Meta:
        unique_together = ('doctor', 'date', 'time') 
    
    def __str__(self):
        return f"Appointment of {self.patient.Name} with {self.doctor.Name} on {self.date} at {self.time} ({self.status})"

class RevealRecords(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    roshata_description = models.TextField(max_length=300)
    other_note_about_medicine = models.TextField(max_length=300)
    date = models.DateField()
    
    def __str__(self):
        return f"Record for {self.patient.Name} by {self.doctor.Name} on {self.date}"
