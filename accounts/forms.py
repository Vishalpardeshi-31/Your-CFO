from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@student.edu'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'you@student.edu'}))


class FinancialSurveyForm(forms.ModelForm):
    """Form for collecting initial financial survey data during onboarding."""
    
    goals_and_wants = forms.CharField(
        label='Your Goals & Wants',
        help_text='Enter your financial goals and wants (e.g., "Car: 500000 by Dec 2026, Vacation: 100000 by Jul 2026")',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'List your goals with amounts and dates'}),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ('monthly_income', 'necessary_needs', 'goals_and_wants', 'monthly_unwanted_limit')
        widgets = {
            'monthly_income': forms.NumberInput(attrs={
                'placeholder': 'e.g., 50000',
                'step': '0.01',
                'min': '0',
                'class': 'form-input'
            }),
            'necessary_needs': forms.NumberInput(attrs={
                'placeholder': 'e.g., 30000 (rent, EMI, groceries)',
                'step': '0.01',
                'min': '0',
                'class': 'form-input'
            }),
            'monthly_unwanted_limit': forms.NumberInput(attrs={
                'placeholder': 'e.g., 5000',
                'step': '0.01',
                'min': '0',
                'class': 'form-input'
            }),
        }
        labels = {
            'monthly_income': 'Monthly Income',
            'necessary_needs': 'Monthly Necessary Expenses (rent, EMI, groceries, etc.)',
            'monthly_unwanted_limit': 'Monthly Limit for Unwanted/Discretionary Spending',
        }
