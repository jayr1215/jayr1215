from django.contrib import admin
from .models import Patient, Appointment, Payment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'cost')
    list_filter = ('status', 'date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount_paid', 'due_amount', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
