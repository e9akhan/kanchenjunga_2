"""
    Module name :- forms
"""

from django import forms
from store.models import EquipmentType, Equipment, Allocation


class EquipmentTypeForm(forms.ModelForm):
    """
        Equipment Type Form
    """
    class Meta:
        """
            Meta class
        """
        model = EquipmentType
        exclude = ('slug',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'threshold': forms.NumberInput(attrs={'class': 'form-control'})
        }


class UpdatequipmentTypeForm(EquipmentTypeForm):
    """
        Update Equipment Type
    """
    class Meta:
        """
            Meta class
        """
        widgets = {
            'abbreviation': forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
        }


class EquipmentForm(forms.ModelForm):
    """
        Equipment Form
    """
    equipment_type = forms.ModelChoiceField(queryset=EquipmentType.objects.all())
    class Meta:
        """
            Meta class
        """
        model = Equipment
        fields = ('label', 'serial_number', 'model_number', 'buy_date', 'equipment_type')

        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'buy_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    equipment_type.widget.attrs.update({'class': 'form-select'})


class UpdateEquipmentForm(EquipmentForm):
    """
        Update Equipment Form
    """
    class Meta(EquipmentForm.Meta):
        """
            Meta class.
        """
        fields = EquipmentForm.Meta.fields + ('functional', 'under_repair')