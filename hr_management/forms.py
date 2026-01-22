from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from .models import Designation, Employee

class DepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields="__all__"

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'department']

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'اسم التسمية'
        })
        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'اختر القسم'
        })

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}))

class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأول'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأخير'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}))
    phone = forms.CharField(max_length=13, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}))
    gender = forms.ChoiceField(choices=Employee.choiceGender, widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(min_value=18, max_value=50, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'العمر'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Employee.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                gender=self.cleaned_data['gender'],
                age=self.cleaned_data['age']
            )
        return user

class ReportForm(forms.ModelForm):
    # Show only the employee's first_name in the choice list
    class EmployeeChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.first_name

    first_name = EmployeeChoiceField(queryset=Employee.objects.all(), label='first_name', empty_label='اختر موظف')

    class Meta:
        model = Report
        fields = ['first_name', 'title', 'description']
