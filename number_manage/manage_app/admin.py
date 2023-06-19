from django import forms
from django.contrib import admin
from django.db import models
from .models import Customer, Business, MobileNumber, MobileNumberAllocation, LandlineNumber, LandlineNumberAllocation, AreaCode, MobilePrefix
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q

@admin.register(LandlineNumber)
class LandlineNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'actual_number', 'province', 'area', 'carrier', 'supplier', 'isenabled', 'update_time', 'create_time')
    list_filter = ('province', 'area', 'carrier', 'supplier', 'isenabled', 'update_time', 'create_time')
    list_per_page = 25
    search_fields = ('number', 'actual_number', 'province', 'area', 'carrier', 'supplier', 'isenabled')
    fieldsets = (
        ('Main', {
            'fields': ('number', 'actual_number', 'supplier', 'isenabled'),
        }),
    )


class LandlineNumberAllocationForm(forms.ModelForm):
    business = forms.ModelChoiceField(queryset=Business.objects.all(), label='业务')

    class Meta:
        model = LandlineNumberAllocation
        fields = '__all__'

'''
class PaginatedFilteredSelectMultiple(forms.SelectMultiple):
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.per_page = 10  # 每页显示的选项数量
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['class'] = 'selectfilter'
        output = super().render(name, value, attrs, renderer)
        return output

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return values[:self.per_page]  # 仅返回每页的选项
'''

class CustomLandlineNumberAllocationAdmin(admin.ModelAdmin):
    list_display = ('business', 'isenabled', 'update_time', 'create_time')
    search_field = ('business')
    fieldset = (
        ('Main', {
            'fields': ('business'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    filter_horizontal = ('numbers',)
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': PaginatedFilteredSelectMultiple(verbose_name='', is_stacked=False)},
    # }

    def get_form(self, request, obj=None, **kwargs):
        self.form = LandlineNumberAllocationForm
        return super().get_form(request, obj, **kwargs)


@admin.register(LandlineNumberAllocation)
class LandlineNumberAllocationAdmin(CustomLandlineNumberAllocationAdmin):
    pass





@admin.register(MobileNumber)
class MobileNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'province', 'area', 'prefix', 'isenabled', 'update_time', 'create_time')
    search_fields = ('number', 'province', 'area', 'prefix')
    fieldsets = (
        ('Main', {
            'fields': ('number', 'prefix'),
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_account', 'customer_full_name', 'customer_rate', 'isenabled', 'update_time', 'create_time')
    search_fields = ('customer_account', 'customer_full_name', 'customer_rate')
    fieldsets = (
        ('Main', {
            'fields': ('customer_account', 'customer_full_name', 'customer_rate'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('customer', 'business_name', 'business_full_name', 'isenabled', 'update_time', 'create_time')
    # 查找报错，TODO
    # search_fields = ('customer', 'business_name', 'business_full_name')
    # fieldsets = (
    #     ('Main', {
    #         'fields': ('customer', 'business_name', 'business_full_name'),
    #     }),
    #     ('Advanced', {
    #         'classes': ('collapse',),
    #         'fields': (),
    #     }),
    # )

@admin.register(MobileNumberAllocation)
class MobileNumberAllocationAdmin(admin.ModelAdmin):
    list_display = ('business', 'isenabled', 'update_time', 'create_time')
    search_field = ('business')
    fieldset = (
        ('Main', {
            'fields': ('business'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )

@admin.register(AreaCode)
class AreaCodeAdmin(admin.ModelAdmin):
    list_display = ('province', 'area', 'code')
    search_fields = ('province', 'area', 'code')
    fieldsets = (
        ('Main', {
            'fields': ('province', 'area', 'code'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )

@admin.register(MobilePrefix)
class MobilePrefixAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'province', 'area', 'code', 'carrier')
    search_fields = ('prefix', 'province', 'area', 'code', 'carrier')
    fieldsets = (
        ('Main', {
            'fields': ('prefix', 'province', 'area', 'code', 'carrier'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )