from django import forms
from django.contrib.auth.models import User
from .models import Expense
from .import views
from django.core.validators import MinLengthValidator

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'maxlength': '20',
            'minlength': '8' 
        }),
        validators=[MinLengthValidator(8)],
        max_length=20
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'maxlength': '20',
            'minlength': '8'
        }),
        validators=[MinLengthValidator(8)],
        max_length=20 
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]


    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Calendar function
        }
        # widgets = {
        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control form-control-sm',
        #         'rows': 2,
        #     }),
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})