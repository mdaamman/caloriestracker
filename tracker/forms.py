from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Food, DailyFoodLog


class UserRegistrationForm(UserCreationForm):
    """
    Extended user registration form with email field.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name (optional)'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name (optional)'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for creating/updating user profile with physical attributes.
    """
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height', 'weight', 'activity_level']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age in years',
                'min': 1,
                'max': 120
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm',
                'step': '0.01',
                'min': 0
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.01',
                'min': 0
            }),
            'activity_level': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'age': 'Age (years)',
            'gender': 'Gender',
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'activity_level': 'Activity Level',
        }
        help_texts = {
            'activity_level': 'Select your daily activity level to calculate accurate calorie needs.',
        }


class FoodLogForm(forms.ModelForm):
    """
    Form for logging daily food consumption.
    """
    food = forms.ModelChoiceField(
        queryset=Food.objects.all().order_by('category', 'name'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'food-select'
        }),
        label='Food Item'
    )
    
    class Meta:
        model = DailyFoodLog
        fields = ['food', 'quantity', 'date']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity in grams',
                'step': '0.01',
                'min': 0.01,
                'id': 'quantity-input'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'date-input'
            }),
        }
        labels = {
            'food': 'Food Item',
            'quantity': 'Quantity (grams)',
            'date': 'Date',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['date'].initial = timezone.now().date()


class LoginForm(forms.Form):
    """
    Simple login form for user authentication.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
