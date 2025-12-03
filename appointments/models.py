from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):

    name = models.CharField(max_length=150)
    area = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    available_from = models.TimeField()
    available_to = models.TimeField()

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Leave', 'On Leave')
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return self.name


class Appointment(models.Model):

    patient_name = models.CharField(max_length=120)
    patient_phone = models.CharField(max_length=12)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    token_number = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token_number} - {self.patient_name}"

class StaffProfile(models.Model):

    ROLE_CHOICES = [
        ('SuperAdmin','Super Admin'),
        ('Reception','Reception Staff')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.hospital.name}"
