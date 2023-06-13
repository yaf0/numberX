from django.shortcuts import render, redirect
from .models import MobileNumber
from datetime import datetime


'''
def success_page(request):
    # 从数据库中获取最新创建的 MobileNumber 对象
    mobile_number = MobileNumber.objects.latest('create_time')

    # 构造上下文字典，包含需要在模板中显示的数据
    context = {
        'mobile_number': mobile_number.number,
        'province': mobile_number.province,
        'area': mobile_number.area,
        'prefix': mobile_number.prefix,
        'is_enabled': mobile_number.isenabled,
        'create_time': mobile_number.create_time,
        'update_time': mobile_number.update_time,
    }

    return render(request, 'success_page.html', context)

def MobileNumberListView(request):
    numbers = MobileNumber.objects.filter()
    context = {
        'numbers': numbers
    }
    return render(request, 'number_list.html', context)



def SubmitMobileNumber(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        province = request.POST.get('province')
        area = request.POST.get('area')
        prefix = request.POST.get('prefix')
        isenabled = bool(request.POST.get('isenabled'))
        
        # 生成当前时间作为创建时间和更新时间
        create_time = datetime.now()
        update_time = create_time

        # 检查必填项是否有值
        if not (number and province and area):
            return render(request, 'invalid_form.html')

        # 创建 MobileNumber 对象并保存
        mobile_number = MobileNumber(
            number=number,
            province=province,
            area=area,
            prefix=prefix,
            isenabled=isenabled,
            update_time=update_time,
            create_time=create_time
        )
        mobile_number.save()

        return redirect('success_page')

    return render(request, 'submit_mobile_number.html')


from django.shortcuts import render
from .models import LandlineNumber, MobileNumber, Customer, Business, LandlineNumberAllocation, MobileNumberAllocation

def landline_number_management(request):
    x_numbers = LandlineNumber.objects.all()
    context = {
        'x_numbers': x_numbers
    }

    return render(request, 'index.html', context)

def mobile_number_management(request):
    x_numbers = MobileNumber.objects.all()
    context = {
        'x_numbers': x_numbers
    }

    return render(request, 'index.html', context)

def customer_management(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'index.html', context)

def business_management(request):
    businesses = Business.objects.all()
    context = {
        'businesses': businesses
    }
    return render(request, 'index.html', context)

def landline_allocation(request):
    allocations = LandlineNumberAllocation.objects.all()
    context = {
        'allocations': allocations
    }
    return render(request, 'index.html', context)

def mobile_allocation(request):
    allocations = MobileNumberAllocation.objects.all()
    context = {
        'allocations': allocations
    }
    return render(request, 'index.html', context)
'''


from django.shortcuts import render
from .models import LandlineNumber, MobileNumber, Customer, Business

def index(request):
    landline_numbers = LandlineNumber.objects.all()
    mobile_numbers = MobileNumber.objects.all()
    customers = Customer.objects.all()
    businesses = Business.objects.all()
    
    context = {
        'landline_numbers': landline_numbers,
        'mobile_numbers': mobile_numbers,
        'customers': customers,
        'businesses': businesses,
    }
    
    return render(request, 'index.html', context)