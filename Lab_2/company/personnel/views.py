from datetime import date

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from personnel.settings import RETIREMENT_AGE_FEMALE
from personnel.forms import *
from personnel.models import *

# Create your views here.

def index(request):
    return render(
        request,
        'index.html',
        context={}
    )

def employee(request):
    table = [employee.get_table_fields()
        for employee in Employee.objects.all()]
    return render(
        request,
        'sections/employee.html',
        context={'table': table}
    )

def add_employee(request):
    personal_form = PersonalEmployeeForm()
    history_form = EmployeeHistoryAddForm()
    return render(
        request,
        'sections/add_employee.html',
        context={
            'personal_form': personal_form,
            'history_form': history_form,
            }
    )

def add_employee_action(request):
    if request.method == "POST":
        personal_form = PersonalEmployeeForm(request.POST)
        history_form = EmployeeHistoryAddForm(request.POST)
        if personal_form.is_valid() \
            and history_form.is_valid():
            date_ = date(
                year = int(request.POST['birth_date_year']),
                month = int(request.POST['birth_date_month']),
                day = int(request.POST['birth_date_day'])
            )
            employee = Employee(
                first_name=request.POST['first_name'],
                second_name=request.POST['second_name'],
                patronymic=request.POST['patronymic'],
                sex=request.POST['sex'],
                birth_date=date_,
                marital_status=request.POST['marital_status'],
            )
            employee.save()

            history=EmployeeHistory(
                employee=employee,
                department=get_object_or_404(
                    Department,
                    id=request.POST['department']
                ),
                post=get_object_or_404(Post, id=request.POST['post']),
                rank=request.POST['rank'],
                start_date=datetime.now().date(),
                end_date=None
            )

            history.save()

            personal_form.clean()
            history_form.clean()

            return redirect('add-employee')

    else:
        personal_form = PersonalEmployeeForm()
        history_form = EmployeeHistoryAddForm()
    return render(
        request,
        'sections/add_employee.html',
        context={
            'personal_form': personal_form,
            'history_form': history_form,
        }
    )

def employee_history(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee_history = EmployeeHistory.objects.filter(
        employee_id=employee_id
    )
    table = list()
    for history_interval in employee_history:
        table.append([
            history_interval.department,
            history_interval.post, 
            history_interval.rank,
            history_interval.start_date,
            history_interval.end_date if history_interval.end_date
                != None else "----"  
        ])
    return render(
        request,
        'sections/employee_history.html',
        context={
            'table': table,
            'employee': employee
            }
    )

def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    personal_form = PersonalEmployeeForm(
        initial={
            'first_name': employee.first_name,
            'second_name': employee.second_name,
            'patronymic': employee.patronymic,
            'sex': employee.sex,
            'birth_date': employee.birth_date,
            'marital_status': employee.marital_status
        })
    return render(
        request,
        'sections/edit_employee.html',
        context={'personal_form': personal_form}
    )

def edit_employee_action(request, employee_id):
    if request.method == "POST":
        form = PersonalEmployeeForm(request.POST)
        if form.is_valid():
            employee = Employee.objects.filter(pk=employee_id)
            date_ = date(
                year=int(request.POST['birth_date_year']),
                month=int(request.POST['birth_date_month']),
                day=int(request.POST['birth_date_day'])
            )
            employee.update(
                first_name=request.POST['first_name'],
                second_name=request.POST['second_name'],
                patronymic=request.POST['patronymic'],
                birth_date=date_,
                sex=request.POST['sex'],
                marital_status=request.POST['marital_status']
            )
        return redirect('employee')

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(
        request,
        'sections/delete_employee.html',
        context={
            'employee_id': employee_id,
            'employee': employee
        }
    )

def delete_employee_action(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    return redirect('employee')

def transfers(request):
    if request.method == "POST":
        search_form = EmployeeSearchForm(request.POST)
        if search_form.is_valid():
            employee = get_object_or_404(
                Employee,
                first_name=request.POST['first_name'],
                second_name=request.POST['second_name'],
                patronymic=request.POST['patronymic']
                )
            return HttpResponseRedirect(
                reverse(
                    'transfer-employee',
                    kwargs={'employee_id': employee.id}
                )
            )
    else:
        search_form = EmployeeSearchForm()
    return render(
        request,
        'sections/transfers.html',
        context={
            'search_form': search_form
        }
    )

def transfer_employee(request, employee_id):
    prev_employee_history = EmployeeHistory.objects.filter(
        employee_id=employee_id
    )
    prev_employee_history = prev_employee_history.order_by('-id')[0]
    if request.method == 'POST':
        history_form = EmployeeHistoryEditForm(request.POST)
        if history_form.is_valid():
            new_employee_history = EmployeeHistory(
                employee_id=prev_employee_history.employee_id,
                department=Department.objects.filter(
                        pk=request.POST['department']
                    )[0],
                post=Post.objects.filter(
                        pk=request.POST['post']
                    )[0],
                rank=int(request.POST['rank']),
                start_date=datetime.strptime(
                    request.POST['start_date'],
                    '%d.%m.%Y'
                ),
                end_date=datetime.strptime(
                    request.POST['end_date'],
                    '%d.%m.%Y'
                )
            )
            new_employee_history.save()
            return redirect('transfers')
    else:
        history_form = EmployeeHistoryEditForm(
            initial={
                'department': prev_employee_history.department,
                'post': prev_employee_history.post,
                'rank': prev_employee_history.rank,
                'start_date': prev_employee_history.start_date,
                'end_date':datetime.now().date()
        })
        return render(
            request,
           'sections/transfer_employee.html',
            context={
                'history_form': history_form
            }
        )

def schedule(request):
    schedules = Schedule.objects.all()
    table = []
    for schedule_list in schedules:
        table.append([
            schedule_list.department.name,
            schedule_list.post.name,
            schedule_list.post_count,
            schedule_list.shift_start,
            schedule_list.shift_end
        ])
    return render(
        request,
        'sections/schedule.html',
        context={
            'table': table
        }
    )

def search(request):
    return render(
        request,
        'sections/search.html',
        context={
        }
    )

def retirement_search(request):
    if request.method == "POST":
        search_form = RetirementSearchForm(request.POST)
        if search_form.is_valid():
            max_retirement_birth_year =datetime.now().date().year 
            - RETIREMENT_AGE_FEMALE
            employees = Employee.objects.filter(
                employeehistory__department=request.POST['department'],
                sex='FEMALE',
                birth_date__year__lt=max_retirement_birth_year,
                )
            table = []
            for employee in employees:
                table.append([
                    employee.second_name,
                    employee.first_name,
                    employee.patronymic,
                    employee.birth_date
                ])
            return render(
                request,
                'sections/search_results.html',
                context={
                    'table': table
                }
            )
    else:
        search_form = RetirementSearchForm()
    return render(
        request,
        'sections/retirement_search.html',
        context={
            'search_form': search_form
        }
    )

def age_search(request):
    if request.method == "POST":
        search_form = AgeSearchForm(request.POST)
        if search_form.is_valid():
            max_birth_year = datetime.now().date().year - (int)(request.POST['age'])
            employees = Employee.objects.filter(
                employeehistory__post=request.POST['post'],
                birth_date__year__gt=max_birth_year,
                )
            table = []
            for employee in employees:
                table.append([
                    employee.second_name,
                    employee.first_name,
                    employee.patronymic,
                    employee.birth_date
                ])
            return render(
                request,
                'sections/search_results.html',
                context={
                    'table': table
                }
            )
    else:
        search_form = AgeSearchForm()
    return render(
        request,
        'sections/age_search.html',
        context={
            'search_form': search_form
        }
    )