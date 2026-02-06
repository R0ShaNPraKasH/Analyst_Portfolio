from django import forms
from django.contrib.auth.models import User
from .models import Customer

class RegisterForm(forms.ModelForm):
    # We add extra fields that aren't in the default User model
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, help_text="4-digit PIN")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        # Save the User first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Then create the Customer profile with the PIN
            import random
            random_account = str(random.randint(1000000000, 9999999999)) # Generate 10-digit Account No
            Customer.objects.create(
                user=user,
                pin=self.cleaned_data['pin'],
                account_number=random_account
            )
        return user
    
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, help_text="Enter PIN to confirm")

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, help_text="Enter PIN to confirm")

class TransferForm(forms.Form):
    receiver_account = forms.CharField(max_length=10, help_text="Enter 10-digit Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)

class LoanForm(forms.Form):
    # This line is wrong for forms, let me fix it below
    # CORRECT VERSION:
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Loan Amount")
    net_worth = forms.DecimalField(max_digits=15, decimal_places=2, label="Your Current Net Worth")
    reason = forms.CharField(widget=forms.Textarea, label="Reason for Loan")