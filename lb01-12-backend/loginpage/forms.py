from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    IDENTITY_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
    ]
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    identity = forms.ChoiceField(choices=IDENTITY_CHOICES, widget=forms.Select)
    balance = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, required=False)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Save the profile with additional fields
            Profile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                identity=self.cleaned_data['identity'],
                balance=self.cleaned_data.get('balance') or 0.0
            )
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists. Try again.")
        return email
