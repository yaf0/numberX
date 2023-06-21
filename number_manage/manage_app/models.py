from django.db import models 
from django import forms

class Supplier(models.Model):
    supplier = models.CharField(max_length=40, verbose_name='供应商')
    customer_full_name = models.CharField(
        max_length=80, null=True, verbose_name='全名/备注')
    supplier_rate = models.FloatField(null=True, verbose_name='结算费率')
    concurrency = models.FloatField(null=True, verbose_name='线路并发')
    caps = models.FloatField(null=True, verbose_name='CAPS')
    supplier_ip = models.CharField(max_length=40, null=True, verbose_name='IP')
    supplier_port = models.CharField(max_length=40, null=True, verbose_name='端口')
    supplier_ip2 = models.CharField(max_length=40, null=True, verbose_name='IP2')
    supplier_ip2_port = models.CharField(max_length=40, null=True, verbose_name='IP2端口')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.supplier
    class Meta:
        managed = True
        # db_table = 'manage_app_customer'
        unique_together = (('supplier', 'supplier_rate'),)
        verbose_name = '客户'
        verbose_name_plural = '客户'


class AreaCode(models.Model):
    province = models.CharField(max_length=20, verbose_name='省份')
    area = models.CharField(max_length=20, verbose_name='地区')
    code = models.IntegerField(primary_key=True, verbose_name='区号')

    def __str__(self):
        return self.code
    class Meta:
        managed = True
        db_table = 'manage_app_area_code'    
        verbose_name = '区号省市'
        verbose_name_plural = '区号省市'

class MobilePrefix(models.Model):
    prefix =  models.CharField(max_length=20, primary_key=True, verbose_name='手机号段')
    province = models.CharField(max_length=20, verbose_name='省份')
    area = models.CharField(max_length=20, verbose_name='地区')
    carrier = models.CharField(max_length=20, verbose_name='运营商')
    code = models.IntegerField(verbose_name='区号')

    def __str__(self):
        return self.prefix
    class Meta:
        managed = True
        db_table = 'manage_app_mobile_prefix'
        verbose_name = '手机省市'
        verbose_name_plural = '手机省市'

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
        managed = True
        # db_table = 'manage_app_customer'
        unique_together = (('customer_account', 'customer_rate'),)
        verbose_name = '客户'
        verbose_name_plural = '客户'




class LandlineNumber(models.Model):
    number = models.CharField(
        max_length=40, primary_key=True, verbose_name='号码')
    actual_number = models.CharField(max_length=40, verbose_name='实号码')
    province = models.CharField(max_length=40, null=True, verbose_name='省份')
    area = models.CharField(max_length=40, null=True, verbose_name='地区')
    area_code = models.IntegerField(default=None,verbose_name='区号')
    carrier = models.CharField(max_length=40, null=True, verbose_name='运营商')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.DO_NOTHING, verbose_name='供应商')
    inbound = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, verbose_name='呼入客户')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='下号时间')
    def __str__(self):
        return self.number
    class Meta:
        managed = True
        # db_table = 'manage_app_landlinenumber'
        verbose_name = '固话号码'
        verbose_name_plural = '固话号码'


class MobileNumber(models.Model):
    number = models.CharField(
        max_length=40, primary_key=True, verbose_name='号码')
    province = models.CharField(max_length=40, verbose_name='省份')
    area = models.CharField(max_length=40, verbose_name='地区')
    area_code = models.IntegerField(default=None,verbose_name='区号')
    prefix = models.CharField(max_length=40, verbose_name='前缀')
    inbound = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, verbose_name='呼入客户')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='下号时间')
    def __str__(self):
        return self.number
    class Meta:
        managed = True
        # db_table = 'manage_app_mobilenumber'
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
        managed = True
        # db_table = 'manage_app_business'
        unique_together = (('customer', 'business_name'),)
        verbose_name = '业务'
        verbose_name_plural = '业务'

class CustomLandlineNumberField(models.ManyToManyField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': CustomLandlineNumberFormField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

class CustomLandlineNumberFormField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.filter(inbound__isnull=True)

class LandlineNumberAllocation(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name='客户-业务')

    numbers = CustomLandlineNumberField(LandlineNumber, verbose_name='固话号码')
    inbound = models.BooleanField(default=False, verbose_name='是否呼入')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.business.business_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 获取业务对应的客户
        customer = self.business.customer

        if self.inbound:    

            # 更新固话号码的inbound字段
            for number in self.numbers.all():
                if number.inbound == None:
                    number.inbound = customer
                    number.save()
                else:
                    raise Exception("存在呼入已分配的号码")
        else:
            for number in self.numbers.all():
                if number.inbound == customer:
                    number.inbound = None

    class Meta:
        managed = True
        # db_table = 'manage_app_landlinenumberallocation'
        unique_together = [['business']]
        verbose_name = '固话号码分配'
        verbose_name_plural = '固话号码分配'

#class LandlineNumberAllocationForm(forms.ModelForm):
#    numbers = forms.ModelChoiceField(
#        queryset=LandlineNumber.objects.filter(inbound__isnull=True),
#        widget=forms.CheckboxSelectMultiple
#    )
#    
#    class Meta:
#        model = LandlineNumberAllocation
#        fields = ['business', 'numbers', 'inbound', 'isenabled']

class MobileNumberAllocation(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name='客户-业务')
    numbers = models.ManyToManyField(MobileNumber, verbose_name='手机号码')
    inbound = models.BooleanField(default=False, verbose_name='是否呼入')
    isenabled = models.BooleanField(default=True, verbose_name='是否启用')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def __str__(self):
        return self.business.business_name
    class Meta:
        managed = True
        # db_table = 'manage_app_mobilenumberallocation'
        unique_together = [['business']]
        verbose_name = '手机号码分配'
        verbose_name_plural = '手机号码分配'

