from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from personnel.settings import MAX_RANK, SEX_CHOICES_RU, MARTIAL_CHOICES_RU
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name    


class Schedule(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    post_count = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return ", ".join([self.department.name, self.post.name])   


class Post(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    upper_border = models.IntegerField()
    lower_border = models.IntegerField()

    def __str__(self):
        return self.name 


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX_CHOICES_RU)
    marital_status = models.CharField(
        max_length=20, choices=MARTIAL_CHOICES_RU
        )

    def __str__(self):
        return " ".join([self.second_name, self.first_name,
            self.patronymic])

    def get_table_fields(self):
        return [
            self.id,
            self.second_name,
            self.first_name, 
            self.patronymic,
            self.get_sex_display(),
            self.birth_date,
            self.get_marital_status_display(),
        ]
    

class EmployeeHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rank = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_RANK),
            MinValueValidator(1)
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True)
