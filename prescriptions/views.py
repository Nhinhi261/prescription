# prescriptions/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription, Medication, Patient, PrescriptionMedication, DoseChecking
from .forms import PrescriptionForm, MedicationForm, PatientForm, DoseCheckingForm
from django.http import JsonResponse
from django.utils import timezone

def home(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'home.html', {'prescriptions': prescriptions})

def prescription_list(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.prescription_date = timezone.now()
            prescription.save()

            selected_medications = request.POST.getlist('medications')

            for medication_id in selected_medications:
                medication = Medication.objects.get(pk=medication_id)
                quantity = request.POST.get(f'quantity_{medication_id}')
                PrescriptionMedication.objects.create(prescription=prescription, medication=medication, quantity=quantity)

            return redirect('prescription_list')
    else:
        form = PrescriptionForm()

    prescription_date = timezone.now()
    prescriptions = Prescription.objects.all()
    patients = Patient.objects.all()
    medications = Medication.objects.all()

    prescription_medications = PrescriptionMedication.objects.select_related('medication').filter(prescription__in=prescriptions)

    return render(request, 'prescriptions/prescription_list.html', {
        'prescriptions': prescriptions,
        'patients': patients,
        'medications': medications,
        'form': form,
        'prescription_date': prescription_date,
        'prescription_medications': prescription_medications,
    })

def prescription_update(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescriptions/prescription_form.html', {'form': form})

def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'DELETE':
        prescription.delete()
        return JsonResponse({'message': 'Xóa thành công.'}, status=204)
    return JsonResponse({'message': 'Không thể xóa đơn kê này.'}, status=400)

# Thông tin thuốc
def medication_list(request):
    medications = Medication.objects.all()
    return render(request, 'medication/medication_list.html', {'medications': medications})

def medication_create(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medication_list')
    else:
        form = MedicationForm()
    return render(request, 'medication/medication_form.html', {'form': form})

def medication_update(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('medication_list')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'medication/medication_form.html', {'form': form})

def medication_delete(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        medication.delete()
        return redirect('medication_list')
    return render(request, 'medications/medication_confirm_delete.html', {'medication': medication})

# Thông tin bệnh nhân
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient/patient_list.html', {'patients': patients})

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patient/patient_form.html', {'form': form})

def patient_update(request, pk):
    patient_instance = get_object_or_404(Patient, pk=pk) 
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient_instance)  
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient_instance)
    return render(request, 'patient/patient_form.html', {'form': form})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'DELETE':
        patient.delete()
        return JsonResponse({'message': 'Xóa thành công.'}, status=204)
    return JsonResponse({'message': 'Không thể xóa bệnh nhân này.'}, status=400)

# Kiểm tra liều dùng
def check_dose(request, prescription_id):
    prescription = Prescription.objects.get(pk=prescription_id)

    # Truy vấn tên thuốc dựa trên đơn thuốc
    prescription_medications = prescription.prescriptionmedication_set.all()

    if request.method == 'POST':
        form = DoseCheckingForm(request.POST)
        if form.is_valid():
            dose_check = form.save(commit=False)
            dose_check.prescription = prescription
            dose_check.save()
            return redirect('prescription_list')
    else:
        form = DoseCheckingForm()
    return render(request, 'doseChecking/doseChecking_list.html', {'form': form, 'prescription': prescription, 'prescription_medications': prescription_medications})

def save_dose_check_result(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Lấy dữ liệu từ yêu cầu Ajax
        patient_weight = float(request.POST.get('patient_weight'))
        prescribed_dose = float(request.POST.get('prescribed_dose'))
        dosage_form = float(request.POST.get('dosage_form'))
        is_dosage_correct = request.POST.get('is_dosage_correct') == 'true'
        prescription_id = int(request.POST.get('prescription_id'))

        prescription = Prescription.objects.get(pk=prescription_id)
        checked_date = timezone.now()
        comments = 'no comments'
        dose_check = DoseChecking(
            prescription=prescription,
            is_dosage_correct=is_dosage_correct,
            checked_date=checked_date,
            comments=comments
        )
        dose_check.save()

        return JsonResponse({'message': 'Kết quả kiểm tra đã được lưu thành công'})
    else:
        return JsonResponse({'message': 'Yêu cầu không hợp lệ'}, status=400)
