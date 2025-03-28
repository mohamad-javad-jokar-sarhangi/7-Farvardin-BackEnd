from django import forms
from .models import UserNotRegister

class UserNotRegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("روستایی", "روستایی"),
        ("راننده", "راننده"),
        ("فروشنده", "فروشنده"),
        ("دهیار-شورا", "دهیار-شورا"),
    ]

    class Meta:
        model = UserNotRegister
        fields = ['name', 'phone', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'}),
        }
    
    # تغییر نقش به یک فیلد انتخابی
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'نقش',
    }))
