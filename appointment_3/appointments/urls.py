from django.urls import path
from . import views


urlpatterns = [

path('', views.user_login, name='home'),
path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


    path('user/register/', views.register, name='register'),

    # Dashboards
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),


    # Appointments
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),

    # Payments
    path('payments/', views.payments, name='payments'),
    path('payments/make/<int:appointment_id>/', views.make_payment, name='make_payment'),

    # Admin management
    path('patients/', views.patients, name='patients'),
    path('doctors/', views.doctors, name='doctors'),
    path('reports/', views.reports, name='reports'),
    path('user-management/', views.user_management, name='user_management'),
]
