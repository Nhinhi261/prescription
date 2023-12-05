def check_dose(actual_dose, max_dose):
    if actual_dose <= max_dose:
        return "Liều dùng an toàn."
    else:
        return "Liều dùng này vượt quá giới hạn, Đề nghị bác sĩ đưa đơn thuốc lại cho bệnh nhân."
