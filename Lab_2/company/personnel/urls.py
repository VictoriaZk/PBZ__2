from django.conf.urls import url
from django.urls import path
from personnel import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('employee/', views.employee, name='employee'),


    path(
        'employee/add_employee/',
        views.add_employee,
        name='add-employee'
    ),
    path(
        'employee/add_employee/add/',
        views.add_employee_action,
        name='add-employee-action'
    ),
    path(
        'employee/history_<int:employee_id>/',
        views.employee_history,
        name='employee-history'
    ),
    path(
        'employee/edit_employee_<int:employee_id>/',
        views.edit_employee,
        name='edit-employee'
    ),
    path(
        'employee/edit_employee_<int:employee_id>/edit/',
        views.edit_employee_action,
        name='edit-employee-action'
    ),
    path(
        'employee/delete_employee_<int:employee_id>/',
        views.delete_employee, name='delete-employee'
    ),
    path(
        'employee/delete_employee_<int:employee_id>/delete/',
        views.delete_employee_action,
        name='delete-employee-action'
    ),


    path(
        'transfers/',
        views.transfers,
        name='transfers'
    ),
    path(
        'transfers/transfer_employee_<int:employee_id>/',
        views.transfer_employee,
        name='transfer-employee'
    ),
    

    path(
        'schedule/',
        views.schedule,
        name='schedule'
    ),


    path(
        'search/',
        views.search,
        name='search'
    ),
    path(
        'search/retirement/',
        views.retirement_search,
        name='retirement_search'
    ),
    path(
        'search/age/',
        views.age_search,
        name='age_search'
    ),
]
