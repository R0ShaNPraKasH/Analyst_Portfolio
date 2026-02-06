from django.contrib import admin
from .models import Customer, Transaction, LoanRequest, BankVault

# 1. Custom View for Customers
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'net_worth', 'get_credit_score')
    search_fields = ('account_number', 'user__username')

# 2. Custom View for Loans (To approve/reject)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'reason', 'status')
    list_filter = ('status',) # Filter by Pending/Approved
    actions = ['approve_loan', 'reject_loan']

    # Custom Action: Approve Loan
    def approve_loan(self, request, queryset):
        # We need to give the money to the user when approving
        for loan in queryset:
            if loan.status == 'PENDING':
                # Deduct from Bank Vault
                vault = BankVault.objects.first()
                if vault and vault.total_assets >= loan.amount:
                    vault.total_assets -= loan.amount
                    vault.save()
                    
                    # Add to User Balance
                    loan.customer.balance += loan.amount
                    loan.customer.save()
                    
                    # Update Loan Status
                    loan.status = 'APPROVED'
                    loan.save()
                    
                    # Record Transaction
                    Transaction.objects.create(
                        sender=loan.customer, 
                        amount=loan.amount, 
                        transaction_type='LOAN_RECEIVED'
                    )
                else:
                    self.message_user(request, "Bank does not have enough funds!", level='error')
    
    approve_loan.short_description = "Approve Selected Loans"

# Registering everything
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction)
admin.site.register(LoanRequest, LoanAdmin)
admin.site.register(BankVault)
