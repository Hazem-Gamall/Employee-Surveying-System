from dataclasses import fields
from django.contrib import admin
from .models import Employee
from django import forms
from django.db.models import Q
# Register your models here.

class EmployeeForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=None)    


    def __init__(self, *args, **kwargs):
        """
        Overriding __init__ so we can set up 
        the query set of the employees field with filters
        and perform some filtering on the initial selected values on it
        """

        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['employees'].required = False
        if self.instance.id:            
            children_queryset = self.employees = Employee.objects.exclude(id=self.instance.id).filter(Q(parent=self.instance) | Q(parent__isnull=True))
            if self.instance.parent:
                children_queryset = children_queryset.exclude(id=self.instance.parent.id)
            self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(id=self.instance.id)
            self.fields['employees'].queryset= children_queryset
            self.fields['employees'].initial = self.instance.children
        else:
            self.fields['employees'].queryset= Employee.objects.exclude(parent__isnull=False)

    def clean(self):
        """
        Overriding clean to perform an extra validation check
        on wether the user chose thier parent as a child or not
        if not then we raise a validation error to let the user know
        """

        employee_parent = self.data.get('parent')
        employee_children = self.data.getlist('employees')

        if employee_parent in employee_children:
            raise forms.ValidationError("You can not add the parent as a child")

        return super().clean()
 
    def save(self, commit=True):
        # NOTE: Previously assigned Parents are silently reset

        instance = super(EmployeeForm, self).save(commit=False)
        if instance.id:
                # set parent = None for the previous employees
                self.fields['employees'].initial.update(parent = None)
                
                # set parent = current instance for the newly chosen employees
                self.cleaned_data['employees'].update(parent=instance)
            
        if commit:
            super(EmployeeForm, self).save()
        else:
            return instance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    readonly_fields = ['id']
    list_display = ['id', 'name']

