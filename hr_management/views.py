from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, permission_required 
from .models import *
from .models import Employee
from .forms import DepartmentForm
from .forms import DesignationForm
from .forms import ReportForm

from django.contrib.auth.models import User, Permission
from django.shortcuts import render
from django.contrib import messages
from .models import Designation, Department
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from .models import Report
from .forms import CustomSignupForm
from django.contrib.auth import login as auth_login

# Create your views here.
@login_required
def home(request):
    return render(request,'dashborad.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')



@login_required
def manage_dept(request):
   
    dept=Department.objects.all()
    return render(request,'manage_department.html',{"dept":dept})

@login_required
def your_view(request):
    # username = request.user.username  # الحصول على اسم المستخدم
   return render(request, 'your_template.html', {'username': request.user.username})

@login_required
@permission_required('hr_management.add_department', raise_exception=True)
def add_dept(request):
        form=DepartmentForm()
        if request.method == 'POST':
            form=DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage')
        return render(request,"add_department.html",{'form':form})
@login_required
@permission_required('hr_management.delete_department', raise_exception=True)
def delete_department(request,pk):
    dept=Department.objects.get(id=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('manage')
    context={
        'dept':dept
    }
    return render(request,'delete_department.html',context)

@login_required
@permission_required('hr_management.change_department', raise_exception=True)
def edit_department(request,pk):
    dept=Department.objects.get(id=pk)
    form=DepartmentForm(instance=dept)
    if request.method == 'POST':
        form=DepartmentForm(request.POST,instance=dept)
        if form.is_valid():
            form.save()
            return redirect("manage")
    context={'form':form}
    return render(request,"add_department.html",context)

@login_required
def manage_employee(request):
    employees = Employee.objects.all()
    return render(request, 'manage_employee.html', {'employees': employees})

@login_required
@permission_required('hr_management.add_employee', raise_exception=True)
def add_emp(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_employee')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee
from .forms import EmployeeForm

@login_required
@permission_required('hr_management.change_employee', raise_exception=True)
def edit_employee(request, id):
    # استخدام get_object_or_404 لجلب الموظف أو إظهار خطأ إذا لم يتم العثور عليه
    employee = get_object_or_404(Employee, ID=id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # حفظ البيانات بعد التحقق من صحتها
            return redirect('manage_employee')  # إعادة التوجيه بعد الحفظ
    else:
        form = EmployeeForm(instance=employee)  # إظهار النموذج مع بيانات الموظف الحالية
    
    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


# حذف موظف
@login_required
@permission_required('hr_management.delete_employee', raise_exception=True)
def delete_employee(request, id):
    employee = get_object_or_404(Employee, ID=id)  # استخدام get_object_or_404
    employee.delete()  # الحذف
    return redirect('manage_employee')

@login_required
def manage_designation(request):
    des=Designation.objects.all()
        
    return render(request,'manage_designation.html',{"des":des})

@login_required
@permission_required('hr_management.add_designation', raise_exception=True)
def add_designation(request):
    departments = Department.objects.all()
    error_massage = None
    if request.method == 'POST':
        name = request.POST.get('name')
        id_department = request.POST.get('department')
        # print(f'Name: {name}, Department ID: {id_department}')
        if not name or not id_department:
            error_massage = "All fields are required"
        else:
            try:
                department = Department.objects.filter(id=id_department).first()
                if not department:
                    raise Exception("invalid")
                
                designation = Designation(
                    name=name,
                    department=department
                )
                designation.save()  # تم تصحيح هذا السطر
                # return redirect('manage_designation')
            except Exception as e:
                # print(f"Error: {str(e)}")
                error_massage = str(e)
    
    return render(request, 'add_designation.html', {'departments': departments, 'error': error_massage})

@login_required
@permission_required('hr_management.delete_designation', raise_exception=True)
def delete_designation(request, pk):
    designation = Designation.objects.get(pk=pk)
    if request.method == 'POST':
        designation.delete()
        return redirect('manage_designation')
    return render(request, 'delete_designation.html', {'designation': designation})
    
    # context = {
    #     'designation': designation
    # }
    # return render(request, 'delete_designation.html', context)

@login_required
@permission_required('hr_management.change_designation', raise_exception=True)
def edit_designation(request, pk):
    designation = Designation.objects.get(pk=pk)  # تصحيح الاسم هنا
    form = DesignationForm(instance=designation)  # يجب أن يكون هنا DesignationForm أو النموذج الصحيح
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)  # يجب أن يكون هنا DesignationForm
        if form.is_valid():
            form.save()
            return redirect("manage_designation")
    
    else:
        form = DesignationForm(instance=designation)
    return render(request, 'edit_designation.html', {'form': form, 'designation': designation})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # تحقق من وجود المستخدم
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'هذا الحساب غير موجود.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Grant add/change/delete permissions on login
            for codename in [
                'add_employee','change_employee','delete_employee',
                'add_department','change_department','delete_department',
                'add_designation','change_designation','delete_designation',
                'add_report','change_report','delete_report'
            ]:
                try:
                    perm = Permission.objects.get(codename=codename)
                    user.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    continue
            return redirect('home')  # تغيير إلى اسم الصفحة الرئيسية
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    
    return render(request, 'login.html')



@login_required
def home_view(request):
    return render(request, 'home.html')  # تأكد من وجود ملف home.html

def logout_view(request):
    logout(request)  # تسجيل الخروج
    return redirect('login')  # إعادة توجيه المستخدم إلى صفحة تسجيل الدخول

@login_required
def report_list_view(request):
    reports = Report.objects.all()  # استرجاع جميع التقارير
    return render(request, 'report_list.html', {'reports': reports})

@login_required
@permission_required('hr_management.add_report', raise_exception=True)
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'report_create.html', {'form': form})

@login_required
@permission_required('hr_management.change_report', raise_exception=True)
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'report_edit.html', {'form': form, 'report': report})

@login_required
@permission_required('hr_management.delete_report', raise_exception=True)
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('report_list')
    return render(request, 'report_delete.html', {'report': report})

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Grant add/change/delete permissions on signup
            for codename in [
                'add_employee','change_employee','delete_employee',
                'add_department','change_department','delete_department',
                'add_designation','change_designation','delete_designation',
                'add_report','change_report','delete_report'
            ]:
                try:
                    perm = Permission.objects.get(codename=codename)
                    user.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    continue
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})