import unittest
from django.test import TestCase
from .models import Prescription, DoseChecking, Patient
from .dose_checker import check_dose

class CheckDoseTestCase(TestCase):
    def setUp(self):
        # Create a patient
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            patient_weight=100,  # Patient weight should be a float
            date_of_birth="2000-01-01",
            gender="M",
            contact_number="123456789",
            email="john@example.com",
        )

        # Create a prescription using the patient
        self.prescription = Prescription.objects.create(
            patient=self.patient,
            doctor="Dr. Smith",
            prescription_date="2023-10-17 12:00:00",
        )

    def test_safe_dose(self):
        # Assuming that the actual dose doesn't exceed the limit
        actual_dose = 1  # Less than max_dose
        max_dose = self.patient.patient_weight * 0.1  # 90.5 * 0.1 = 9.05

        result = check_dose(actual_dose, max_dose)
        self.assertEqual(result, "Liều dùng an toàn.")
      

    def test_exceeded_dose(self):
        # Assuming that the actual dose exceeds the limit
        actual_dose = 300  # More than max_dose
        max_dose = self.patient.patient_weight * 0.1  # 90.5 * 0.1 = 9.05

        result = check_dose(actual_dose, max_dose)
        self.assertEqual(result, "Liều dùng này vượt quá giới hạn, Đề nghị bác sĩ đưa đơn thuốc lại cho bệnh nhân.")
  
  

if __name__ == '__main__':
    unittest.main()
