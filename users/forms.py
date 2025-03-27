from django import forms
from .models import UserNotRegister

class UserNotRegisterForm(forms.ModelForm):
    class Meta:
        model = UserNotRegister
        fields = ['name', 'phone', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نقش'}),
        }


