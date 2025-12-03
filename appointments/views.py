from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Hospital, Doctor, Appointment


# ------------------------------
# LIST ALL HOSPITALS
# ------------------------------
@api_view(['GET'])
def list_hospitals(request):
    hospitals = Hospital.objects.all()
    data = [{'id': h.id, 'name': h.name} for h in hospitals]
    return Response(data)


# ------------------------------
# LIST DOCTORS BY HOSPITAL
# ------------------------------
@api_view(['GET'])
def list_doctors(request, hospital_id):
    doctors = Doctor.objects.filter(hospital_id=hospital_id)
    data = [{'id': d.id, 'name': d.name} for d in doctors]
    return Response(data)


# ------------------------------
# BOOK APPOINTMENT
# ------------------------------
@api_view(['POST'])
def book_appointment(request):

    data = request.data

    try:
        doctor = Doctor.objects.get(id=data.get("doctor"))
    except:
        return Response({"error": "Invalid doctor"}, status=400)

    date = data.get("date")

    booking_count = Appointment.objects.filter(
        doctor=doctor,
        date=date
    ).count()

    token = f"T-{booking_count + 1}"

    appointment = Appointment.objects.create(
        patient_name=data.get("patient_name"),
        patient_phone=data.get("patient_phone"),
        doctor=doctor,
        date=date,
        time=data.get("time"),
        token_number=token
    )

    return Response({
        "message": "Appointment booked",
        "token": token
    }, status=status.HTTP_201_CREATED)


from django.shortcuts import render

def homepage(request):
    return render(request, "index.html")
