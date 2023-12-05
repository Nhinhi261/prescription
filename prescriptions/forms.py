# prescriptions/forms.py

from django import forms
from .models import Prescription, Medication, Patient, DoseChecking

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('patient', 'doctor', 'prescription_date')

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ('name', 'description', 'active_ingredient', 'manufacturer', 'dosage_form', 'prescribed_dose', 'unit_price', 'stock_quantity')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'patient_weight', 'date_of_birth', 'gender', 'contact_number', 'email')

class DoseCheckingForm(forms.ModelForm):
    class Meta:
        model = DoseChecking
        fields = ['is_dosage_correct', 'comments']