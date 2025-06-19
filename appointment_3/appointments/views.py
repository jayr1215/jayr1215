from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Patient, Appointment, Payment
from .forms import AppointmentForm, UserRegisterForm, PatientProfileForm
from django.contrib.auth.models import User
from django.contrib import messages # Add this line

def get_monthly_data(model, date_field):
    now = timezone.now()
    return model.objects.filter(**{
        f"{date_field}__month": now.month,
        f"{date_field}__year": now.year
    })

# --- Authentication ---

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on role
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'appointments/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/') # Redirect to the home page after logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']

            if role == 'admin':
                user.is_staff = True  # Give admin rights
            else:
                user.is_staff = False  # Make sure patients are NOT staff

            user.save()

            if role == 'patient':
                Patient.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'appointments/register.html', {'form': form})

# --- Dashboards ---

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return render(request, 'appointments/user_dashboard.html')

    appointments = Appointment.objects.filter(patient=patient) if patient else Appointment.objects.none()
    payments = Payment.objects.filter(appointment__patient=patient) if patient else Payment.objects.none()

    total_amount_paid = sum(payment.amount_paid for payment in payments)
    total_due_amount = sum(payment.due_amount for payment in payments)
    completed_payments = payments.filter(status='completed').count()
    pending_payments = payments.filter(status='pending').count()

    notifications = ["Appointment reminder", "Payment due"]
    health_records = ["Blood Test - Normal", "X-ray - Clear"]

    context = {
        'user': user,
        'appointments': appointments,
        'total_amount_paid': total_amount_paid,
        'total_due_amount': total_due_amount,
        'completed_payments': completed_payments,
        'pending_payments': pending_payments,
        'notifications': notifications,
        'health_records': health_records,
    }
    return render(request, 'appointments/user_dashboard.html', context)

@login_required(login_url='Admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    return render(request, 'appointments/admin_dashboard.html')

    upcoming_appointments = Appointment.objects.filter(date__gte=timezone.now()).order_by('date')
    appointments = Appointment.objects.all()
    payments = Payment.objects.all()
    users = Patient.objects.all()

    monthly_appointments = get_monthly_data(Appointment, 'date').count()
    monthly_income = sum(payment.amount_paid for payment in get_monthly_data(Payment, 'payment_date'))

    context = {
        'total_appointments': appointments.count(),
        'total_payments': payments.count(),
        'total_users': users.count(),
        'monthly_appointments': monthly_appointments,
        'upcoming_appointments': upcoming_appointments,
        'monthly_income': monthly_income,
    }
    return render(request, 'appointments/admin_dashboard.html', context)

# --- Appointments ---

@login_required(login_url='user_login')
def appointments(request):
    if request.user.is_staff:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'appointments/appointment_table.html', {'appointments': appointments})

@login_required(login_url='user_login')
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            # Ensure a Patient object exists for the user
            if not hasattr(request.user, 'patient'):
                from .models import Patient  # Import Patient model here to avoid circular dependency
                patient = Patient.objects.create(user=request.user)
                request.user.patient = patient
            
            appointment.patient = request.user.patient
            appointment.save()

            # Update patient's profile with new information
            patient_profile = request.user.patient
            patient_profile.name = form.cleaned_data['name']
            patient_profile.age = form.cleaned_data['age']
            patient_profile.phone_number = form.cleaned_data['phone_number']
            patient_profile.email = form.cleaned_data['email']
            patient_profile.save()

            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

# --- Payments ---

@login_required(login_url='user_login')
def payments(request):
    user = request.user
    if user.is_staff:
        payments = Payment.objects.all()
    else:
        try:
            patient = user.patient
            payments = Payment.objects.filter(appointment__patient=patient)
        except Patient.DoesNotExist:
            payments = Payment.objects.none()
    return render(request, 'appointments/payments.html', {'payments': payments})

@login_required(login_url='user_login')
def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        amount_paid = float(request.POST.get('amount_paid', 0))
        due_amount = float(request.POST.get('due_amount', 0))
        status = request.POST.get('status', 'pending')

        payment = Payment(
            appointment=appointment,
            amount_paid=amount_paid,
            due_amount=due_amount,
            status=status,
        )
        payment.save()
        return redirect('payments')
    return render(request, 'appointments/make_payment.html', {'appointment': appointment})

# --- Admin management ---

@login_required(login_url='user_login')
def patients(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    all_patients = Patient.objects.all()
    context = {'all_patients': all_patients}
    return render(request, 'appointments/manage_patients.html', context)

@login_required(login_url='user_login')
def doctors(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    all_doctors = User.objects.filter(is_staff=True)
    context = {'all_doctors': all_doctors}
    return render(request, 'appointments/manage_doctors.html', context)

@login_required(login_url='user_login')
def reports(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    report_data = {
        "appointments": Appointment.objects.count(),
        "payments": Payment.objects.count()
    }
    return render(request, 'appointments/reports.html', {'report_data': report_data})

@login_required(login_url='user_login')
def user_management(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    users = Patient.objects.all()
    return render(request, 'appointments/user_management.html', {'users': users})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
