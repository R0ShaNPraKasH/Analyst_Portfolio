from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, DepositForm, WithdrawForm, TransferForm, LoanForm
from .models import Transaction, BankVault, LoanRequest
from django.db import transaction


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def dashboard(request):
    try:
        # Get the 'Customer' object linked to the logged-in User
        customer = request.user.customer
        
        # Calculate credit score dynamically
        credit_score = customer.get_credit_score()
        
        context = {
            'customer': customer,
            'credit_score': credit_score,
            'is_vip': customer.has_lounge_access() # Check for lounge access
        }
        return render(request, 'dashboard.html', context)
    except Customer.DoesNotExist:
        # Fallback if something went wrong during registration
        return render(request, 'base.html', {'message': "Customer data not found."})
    

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            pin = form.cleaned_data['pin']
            customer = request.user.customer

            # 1. Verify PIN
            if pin != customer.pin:
                messages.error(request, "Invalid PIN!")
                return redirect('deposit')

            # 2. Add Money
            customer.balance += amount
            customer.save()

            # 3. Create Transaction Record
            Transaction.objects.create(
                sender=customer,
                receiver=None, # No receiver for deposits
                amount=amount,
                transaction_type='DEPOSIT'
            )

            messages.success(request, f"Successfully deposited ₹{amount}!")
            return redirect('dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'deposit.html', {'form': form})


@login_required
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            pin = form.cleaned_data['pin']
            customer = request.user.customer

            # 1. Verify PIN
            if pin != customer.pin:
                messages.error(request, "Invalid PIN!")
                return redirect('withdraw')

            # 2. ANTI-ERROR CHECK: Insufficient Funds
            if customer.balance < amount:
                messages.error(request, "Insufficient funds! Transaction declined.")
                return redirect('withdraw')

            # 3. Deduct Money
            customer.balance -= amount
            customer.save()

            # 4. Create Transaction Record
            Transaction.objects.create(
                sender=customer,
                receiver=None, 
                amount=amount,
                transaction_type='WITHDRAW'
            )

            messages.success(request, f"Successfully withdrew ₹{amount}!")
            return redirect('dashboard')
    else:
        form = WithdrawForm()
    
    return render(request, 'withdraw.html', {'form': form})


@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_acc_num = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']
            pin = form.cleaned_data['pin']
            sender = request.user.customer

            # 1. Verify PIN
            if pin != sender.pin:
                messages.error(request, "Invalid PIN!")
                return redirect('transfer')

            # 2. Check Balance
            if sender.balance < amount:
                messages.error(request, "Insufficient funds for transfer.")
                return redirect('transfer')

            # 3. Find Receiver (Error handling if not found)
            try:
                receiver = Customer.objects.get(account_number=receiver_acc_num)
            except Customer.DoesNotExist:
                messages.error(request, "Receiver Account Number does not exist.")
                return redirect('transfer')

            # 4. Atomic Transfer (Safety Lock)
            with transaction.atomic():
                # Deduct from Sender
                sender.balance -= amount
                sender.save()

                # Add to Receiver
                receiver.balance += amount
                receiver.save()

                # Record the Transaction
                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type='TRANSFER'
                )

            messages.success(request, f"Successfully transferred ₹{amount} to {receiver.user.username}!")
            return redirect('dashboard')
    else:
        form = TransferForm()
    
    return render(request, 'transfer.html', {'form': form})


@login_required
def request_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            net_worth = form.cleaned_data['net_worth']
            reason = form.cleaned_data['reason']
            customer = request.user.customer

            # 1. Update Customer's declared Net Worth
            customer.net_worth = net_worth
            customer.save()

            # 2. CHECK: Does the bank have enough money?
            # We get the first (and only) vault or create one if it doesn't exist
            vault, created = BankVault.objects.get_or_create(id=1)
            
            if vault.total_assets < amount:
                messages.error(request, "Loan Rejected: Bank does not have sufficient liquidity.")
                return redirect('dashboard')

            # 3. Create the Request (It stays PENDING until Admin approves)
            LoanRequest.objects.create(
                customer=customer,
                amount=amount,
                reason=reason
            )
            
            messages.success(request, "Loan Application Submitted! Pending Admin Approval.")
            return redirect('dashboard')
    else:
        form = LoanForm()
    
    return render(request, 'loan.html', {'form': form})