from django.contrib import admin
from .models import Hospital, Doctor, Appointment , StaffProfile


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):

    list_display = ('name', 'area', 'contact_number')
    search_fields = ('name', 'area')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Main admin sees all hospitals
        if request.user.is_superuser:
            return qs

        # Doctor sees only own hospital
        try:
            doctor = Doctor.objects.get(user=request.user)
            return qs.filter(id=doctor.hospital.id)
        except:
            pass

        # Reception or SuperAdmin sees only their hospital
        try:
            staff = StaffProfile.objects.get(user=request.user)
            return qs.filter(id=staff.hospital.id)
        except:
            pass

        return qs.none()



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'specialization',
        'hospital',
        'available_from',
        'available_to',
        'status',
    )
    list_filter = ('hospital', 'specialization','status')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Main admin sees all doctors
        if request.user.is_superuser:
            return qs

        # Doctor sees only their own profile
        try:
            doctor = Doctor.objects.get(user=request.user)
            return qs.filter(id=doctor.id)
        except:
            pass

        # Reception / SuperAdmin sees doctors of their hospital
        try:
            staff = StaffProfile.objects.get(user=request.user)
            return qs.filter(hospital=staff.hospital)
        except:
            pass

        return qs.none()



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'token_number',
        'patient_name',
        'doctor',
        'date',
        'time',
        'patient_phone',
        'created_at',
    )
    list_filter = ('doctor','date')
    search_fields = ('patient_name','patient_phone')
    ordering = ('date','time')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Main admin sees all
        if request.user.is_superuser:
            return qs

        # Doctor → only own patients
        try:
            doctor = Doctor.objects.get(user=request.user)
            return qs.filter(doctor=doctor)
        except:
            pass

        # Reception / SuperAdmin → clinic patients
        try:
            staff = StaffProfile.objects.get(user=request.user)
            return qs.filter(doctor__hospital=staff.hospital)
        except:
            pass

        return qs.none()



@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = ('user','hospital','role')
    list_filter = ('hospital','role')
