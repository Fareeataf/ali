from django.contrib import admin
from .models import *
from .models import Report
# Register your models here.

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Report)

