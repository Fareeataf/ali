from django.urls import path
from . import views
# ...existing code...
urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manage-dept/', views.manage_dept, name='manage'),
    path('add-dept/', views.add_dept, name='add_dept'),
    path('edit-department/<int:pk>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:pk>/', views.delete_department, name='delete_department'),
    path('manage-employee/', views.manage_employee, name='manage_employee'),
    path('add-emp/', views.add_emp, name='add_emp'),
    path('employee/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('manage-designation/', views.manage_designation, name='manage_designation'),
    path('add-designation/', views.add_designation, name='add_designation'),
    path('edit-designation/<int:pk>/', views.edit_designation, name='edit_designation'),
    path('delete-designation/<int:pk>/', views.delete_designation, name='delete_designation'),
    path('reports/', views.report_list_view, name='report_list'),
    path('reports/add/', views.create_report, name='report_add'),
    path('reports/edit/<int:pk>/', views.edit_report, name='report_edit'),
    path('reports/delete/<int:pk>/', views.delete_report, name='report_delete'),
]
# ...existing code...