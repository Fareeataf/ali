import os
import sys
import django

# ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ELMS.settings')
django.setup()
from hr_management.models import Employee, Report

e = Employee.objects.first()
if not e:
    print('No employees found — create an employee first')
else:
    r = Report.objects.create(first_name=e, title='تقرير تجريبي', description='وصف تجريبي')
    print('Created report id=', r.pk)
