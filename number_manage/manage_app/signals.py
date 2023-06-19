from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Customer, Business, MobileNumber, MobileNumberAllocation, LandlineNumber, LandlineNumberAllocation, AreaCode, MobilePrefix
import re

def get_area_code(number):
    number = number.lstrip('0')
    match = re.match(r'^((10)|(2\d{1})|([3456789]\d{2}))', number)
    if match:
        return match.group(1)
    return None

def get_prefix_code(number):
    match = re.match(r'^(1[3-9]\d{5})', number)
    if match:
        return match.group(1)
    return None

@receiver(pre_save, sender=LandlineNumber)
def generate_landline_fields(sender, instance, **kwargs):
    number_area_code = get_area_code(instance.number)
    actual_number_area_code = get_area_code(instance.actual_number)

    if number_area_code and actual_number_area_code:
        try:
            number_area = AreaCode.objects.get(code=number_area_code)
            actual_number_area = AreaCode.objects.get(code=actual_number_area_code)
            instance.province = number_area.province
            instance.area = number_area.area
            instance.area_code = number_area.code
            instance.carrier = actual_number_area.area
        except AreaCode.DoesNotExist:
            pass

@receiver(pre_save, sender=MobileNumber)
def generate_mobile_fields(sender, instance, **kwargs):
    number_area_code = get_prefix_code(instance.number)

    if number_area_code:
        try:
            number_area = MobilePrefix.objects.get(prefix=number_area_code)
            instance.province = number_area.province
            instance.area = number_area.area
            instance.area_code = number_area.code
        except AreaCode.DoesNotExist:
            pass