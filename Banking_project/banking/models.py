from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    pin = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_worth = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def get_credit_score(self):
        # Start with 300. Add 10 points for every transaction. Max 850.
        tx_count = Transaction.objects.filter(sender=self).count()
        score = 300 + (tx_count * 10)
        return min(score, 850)
    
    def has_lounge_access(self):
        return self.balance >= 50000

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class Transaction(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_money', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='received_money', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20) # DEPOSIT, WITHDRAW, TRANSFER

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"

class LoanRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='PENDING') # PENDING, APPROVED, REJECTED

    def __str__(self):
        return f"Loan: {self.customer.user.username} - {self.amount}"
    

class BankVault(models.Model):
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=10000000.00) # Bank starts with 1 Crore

    def __str__(self):
        return f"Bank Reserves: ₹{self.total_assets}"