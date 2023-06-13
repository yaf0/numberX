from django import forms
from django.contrib import admin
from .models import Customer, Business, MobileNumber, MobileNumberAllocation, LandlineNumber, LandlineNumberAllocation
from django.contrib.admin.widgets import FilteredSelectMultiple


class LandlineNumberAllocationForm(forms.ModelForm):
    business = forms.ModelChoiceField(queryset=Business.objects.all(), label='业务')

    class Meta:
        model = LandlineNumberAllocation
        fields = '__all__'






class CustomLandlineNumberAllocationAdmin(admin.ModelAdmin):
    list_display = ('business', 'isenabled', 'update_time', 'create_time')
    filter_horizontal = ('numbers',)

    def get_form(self, request, obj=None, **kwargs):
        self.form = LandlineNumberAllocationForm
        return super().get_form(request, obj, **kwargs)




class LandlineNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'actual_number', 'province', 'area', 'carrier', 'supplier', 'isenabled', 'update_time', 'create_time')
    def allocate_to_business(modeladmin, request, queryset):
        selected_business = request.POST.get('business')  # 获取所选的业务ID
        if selected_business:
            business = Business.objects.get(id=selected_business)
            for number in queryset:
                allocation = LandlineNumberAllocation.objects.create(business=business)
                allocation.numbers.add(number)
                allocation.save()
            modeladmin.message_user(request, "固话号码分配成功")
        else:
            modeladmin.message_user(request, "请选择一个业务")

    allocate_to_business.short_description = "分配给业务"  # 动作名称
    actions = [allocate_to_business]  # 将分配给业务的动作添加到动作下拉框中


@admin.register(LandlineNumber)
class LandlineNumberAdmin(LandlineNumberAdmin):
    pass


@admin.register(MobileNumber)
class MobileNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'province', 'area', 'prefix', 'isenabled', 'update_time', 'create_time')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_account', 'customer_full_name', 'customer_rate', 'isenabled', 'update_time', 'create_time')


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('customer', 'business_name', 'business_full_name', 'isenabled', 'update_time', 'create_time')


@admin.register(MobileNumberAllocation)
class MobileNumberAllocationAdmin(admin.ModelAdmin):
    list_display = ('business', 'isenabled', 'update_time', 'create_time')


@admin.register(LandlineNumberAllocation)
class LandlineNumberAllocationAdmin(CustomLandlineNumberAllocationAdmin):
    pass