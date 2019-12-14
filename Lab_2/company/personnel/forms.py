from datetime import datetime, date
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from personnel.models import Department
from personnel.models import Employee
from personnel.models import Post
from personnel.models import EmployeeHistory
from personnel.settings import *

class PersonalEmployeeForm(forms.ModelForm):
    second_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    patronymic = forms.CharField(label='Отчество')
    birth_date = forms.DateField(label='Дата раждения', 
        widget=forms.SelectDateWidget(years=YEARS),
        initial=date(year=YEARS[-1], month=1, day=1)
        )
    sex = forms.ChoiceField(
        label='Пол',
        choices=SEX_CHOICES_RU
        )
    marital_status = forms.ChoiceField(
        label='Семейное положение',
        choices=MARTIAL_CHOICES_RU
        )

    class Meta:
        model = Employee
        exclude = ['history']


class EmployeeHistoryEditForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        label='Подразделение',
        queryset=Department.objects.all()
    )
    post = forms.ModelChoiceField(
        label='Должность',
        queryset=Post.objects.all()
    )
    rank = forms.IntegerField(
        label='Разряд'
    )
    start_date = forms.DateField(
        label='Дата начала работы',
        initial=datetime.now().date()
    )
    end_date = forms.DateField(
        label='Дата окончания работы',
    )

    def clean(self):
        cd = self.cleaned_data
        rank = cd.get('rank')
        post = cd.get('post')
        return cd

    class Meta:
        model = EmployeeHistory
        exclude = ['employee']


class EmployeeHistoryAddForm(EmployeeHistoryEditForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeHistoryEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('end_date')


class EmployeeSearchForm(forms.ModelForm):
    second_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    patronymic = forms.CharField(label='Отчество')

    class Meta:
        model = Employee
        fields = ['first_name', 'second_name', 'patronymic']


class RetirementSearchForm(forms.Form):
    department = forms.ModelChoiceField(
        label='Подразделение',
        queryset=Department.objects.all()
    )

class AgeSearchForm(forms.Form):
    age = forms.IntegerField(
        label='Возраст (лет)',
        validators=[MinValueValidator(MIN_WORK_AGE), MaxValueValidator(100)]
    )
    post = forms.ModelChoiceField(
        label='Должность',
        queryset=Post.objects.all()
    )