from django.contrib import admin
from prescriptions import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # Thông tin thuốc
    path('medication', views.medication_list, name='medication_list'),
    path('medication/new/', views.medication_create, name='medication_create'),
    path('medication/<int:pk>/edit/', views.medication_update, name='medication_update'),
    path('medication/<int:pk>/delete/', views.medication_delete, name='medication_delete'),
    # Thông tin kê đơn thuốc
    path('prescription', views.prescription_list, name='prescription_list'),
    path('prescription/<int:pk>/edit/', views.prescription_update, name='prescription_update'),
    path('prescription/<int:pk>/delete/', views.prescription_delete, name='prescription_delete'),
    # Thông tin bệnh nhân
    path('patient', views.patient_list, name='patient_list'),
    path('patient/new/', views.patient_create, name='patient_create'),
    path('patient/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    # Kiểm tra liều dùng
    path('check_dose/<int:prescription_id>/', views.check_dose, name='check_dose'),
    path('save_dose_check_result/', views.save_dose_check_result, name='save_dose_check_result'),

]
