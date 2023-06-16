from django.db import models


from django.db import models
'''
class AreaCode(models.Model):
    province = models.CharField(max_length=80)
    area = models.CharField(max_length=80)
    code = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"AreaCode(province={self.province}, area={self.area}, code={self.code})"
'''

class Customer(models.Model):
    customer_account = models.CharField(max_length=40, verbose_name='客户账号')
    customer_full_name = models.CharField(
        max_length=80, null=True, verbose_name='客户全名')
    customer_rate = models.FloatField(null=True, verbose_name='客户费率')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.customer_account
    class Meta:
        unique_together = [['customer_account', 'customer_rate']]
        verbose_name = '客户'
        verbose_name_plural = '客户'


class LandlineNumber(models.Model):
    number = models.CharField(
        max_length=40, primary_key=True, verbose_name='号码')
    actual_number = models.CharField(max_length=40, verbose_name='实号码')
    province = models.CharField(max_length=40, verbose_name='省份')
    area = models.CharField(max_length=40, verbose_name='地区')
    carrier = models.CharField(max_length=40, verbose_name='运营商')
    supplier = models.CharField(max_length=40, verbose_name='供应商')
    inbound = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, verbose_name='呼入客户')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True, verbose_name='最后时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='下号时间')
    def __str__(self):
        return f"LandlineNumber(number={self.number}, inbound={self.inbound} isenabled={self.isenabled}, create_time={self.create_time})"
    class Meta:
        verbose_name = '固话号码'
        verbose_name_plural = '固话号码'


class MobileNumber(models.Model):
    number = models.CharField(
        max_length=40, primary_key=True, verbose_name='号码')
    province = models.CharField(max_length=40, verbose_name='省份')
    area = models.CharField(max_length=40, verbose_name='地区')
    prefix = models.CharField(max_length=40, verbose_name='前缀')
    inbound = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, verbose_name='呼入客户')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='下号时间')
    def __str__(self):
        return f"LandlineNumber(number={self.number}, inbound={self.inbound} isenabled={self.isenabled}, create_time={self.create_time})"
    class Meta:
        verbose_name = '手机号码'
        verbose_name_plural = '手机号码'


class Business(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name='客户')
    business_name = models.CharField(max_length=40, verbose_name='客户-业务')
    business_full_name = models.CharField(
        max_length=40, null=True, verbose_name='业务全名/备注')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.business_name
    class Meta:
        unique_together = [['customer', 'business_name']]
        verbose_name = '业务'
        verbose_name_plural = '业务'


class LandlineNumberAllocation(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name='客户-业务')

    numbers = models.ManyToManyField(LandlineNumber, verbose_name='固话号码')

    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.business.business_name
    class Meta:
        unique_together = [['business']]
        verbose_name = '固话号码分配'
        verbose_name_plural = '固话号码分配'


class MobileNumberAllocation(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name='客户-业务')
    numbers = models.ManyToManyField(MobileNumber, verbose_name='手机号码')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.business.business_name
    class Meta:
        unique_together = [['business']]
        verbose_name = '手机号码分配'
        verbose_name_plural = '手机号码分配'

