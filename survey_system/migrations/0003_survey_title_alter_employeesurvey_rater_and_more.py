# Generated by Django 4.1 on 2022-09-07 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_employee_surveys_alter_employee_user'),
        ('survey_system', '0002_alter_employeesurvey_get_rated'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='employeesurvey',
            name='rater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_set', to='employee.employee'),
        ),
        migrations.AlterField(
            model_name='employeesurvey',
            name='submited_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
