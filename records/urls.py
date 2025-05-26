from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Root URL now points to the login page
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_record, name='add'),  # changed from views.add to views.add_record
    path('edit/<int:pk>/', views.edit_record, name='edit_record'), # Ensure name consistency if used elsewhere
    path('delete/<int:pk>/', views.delete_record, name='delete_record'), # Ensure name consistency
]