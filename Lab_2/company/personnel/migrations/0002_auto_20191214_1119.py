# Generated by Django 2.2.7 on 2019-12-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='sex',
            field=models.CharField(choices=[('MALE', 'муж'), ('FEMALE', 'жен')], max_length=10),
        ),
    ]
