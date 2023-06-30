from django.db.models.signals import pre_save
from django.db.models.signals import post_save

from django.dispatch import receiver 
from .models import Customer, Business, MobileNumber, MobileNumberAllocation, LandlineNumber, LandlineNumberAllocation, AreaCode, MobilePrefix
import re
import logging

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


@receiver(post_save, sender=LandlineNumberAllocation)
def update_landline_numbers(sender, instance, **kwargs):
    # 获取业务对应的客户
    customer = instance
    logging.debug(f'customer字段值为{customer}')
    if instance.inbound:
        logging.debug(f'instance.inbound字段值为{instance.inbound}')
        # 更新固话号码的inbound字段
        logging.debug(f'进入循环前numbers群组的值为{instance.numbers.all()}')
        for number in instance.numbers.all():
            logging.debug(f'进入循环时number值为{number}')
            if number.inbound is None:
                logging.debug(f'inbound为真时{number}的inbound值应该为None 当前为{number.inbound}')
                number.inbound = customer
                logging.debug(f'修改后 inbound为真时{number}的inbound值应该为{customer} 当前为{number.inbound}')
                number.save()

    else:
        logging.debug(f'instance.inbound字段值为{instance.inbound}')
        logging.debug(f'进入循环前numbers群组的值为{instance.numbers.all()}')
        for number in instance.numbers.all():
            logging.debug(f'进入循环时number值为{number}')
            if number.inbound == customer:
                logging.debug(f'inbound为假时{number}的inbound值应该为{customer} 当前为{number.inbound}')
                number.inbound = None
                logging.debug(f'修改后 inbound为假时{number}的inbound值应该为None 当前为{number.inbound}')
                number.save()