from django import forms
from .models import UserNotRegister , User

class UserNotRegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("عادی", "عادی"),
        ("راننده", "راننده"),
        ("فروشنده", "فروشنده"),
        ("شورا", "شورا"),
         ("دهیار", "دهیار"),
        
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

class UserApproveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'role', 'username', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}),
        }