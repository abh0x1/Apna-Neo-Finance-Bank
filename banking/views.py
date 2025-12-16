# banking/views.py
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts import models
from .models import Transaction
from .forms import FundTransferForm
from django.contrib import messages
from accounts.models import CustomUser

@login_required
def net_coming_soon(request):
    return render(request, "banking/net_coming_soon.html")

@login_required
def dashboard(request):
    user = request.user
    last_transactions = Transaction.objects.filter(user=user).order_by('-timestamp')[:5]
    return render(request, "banking/dashboard.html", {"user": user, "last_transactions": last_transactions})

@login_required
def netbanking(request):
    return render(request, "banking/netbanking.html")


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, "banking/transaction_history.html", {"transactions": transactions})


@login_required
def fund_transfer(request):
    if request.method == "POST":
        form = FundTransferForm(request.POST)
        if form.is_valid():
            transfer_by = form.cleaned_data['transfer_by']
            receiver_value = form.cleaned_data['receiver_value']
            amount = form.cleaned_data['amount']
            transaction_mode = form.cleaned_data['transaction_mode']
            description = form.cleaned_data['description']

            sender = request.user

            # Receiver lookup based on selected method
            try:
                if transfer_by == 'username':
                    receiver = CustomUser.objects.get(username=receiver_value)
                elif transfer_by == 'account_number':
                    receiver = CustomUser.objects.get(account_number=receiver_value)
                elif transfer_by == 'mobile':
                    receiver = CustomUser.objects.get(mobile=receiver_value)
                elif transfer_by == 'upi':
                    receiver = CustomUser.objects.get(upi_id=receiver_value)
            except CustomUser.DoesNotExist:
                messages.error(request, "Receiver not found.")
                return redirect("banking:fund_transfer")

            if sender == receiver:
                messages.error(request, "You cannot transfer to yourself.")
                return redirect("banking:fund_transfer")

            if sender.balance < amount:
                messages.error(request, "Insufficient balance.")
                return redirect("banking:fund_transfer")

            # Update balances
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            # Record transactions
            Transaction.objects.create(
                user=sender,
                amount=amount,
                transaction_type='DEBIT',
                description=f"To {receiver.username} ({receiver.ifsc_code}) via {transaction_mode}: {description}"
            )
            Transaction.objects.create(
                user=receiver,
                amount=amount,
                transaction_type='CREDIT',
                description=f"From {sender.username} ({sender.ifsc_code}) via {transaction_mode}: {description}"
            )

            messages.success(request, f"₹{amount} successfully transferred to {receiver.username}.")
            return redirect("banking:dashboard")
    else:
        form = FundTransferForm()

    return render(request, "banking/fund_transfer.html", {"form": form})

@login_required
def virtual_card_view(request):
    user = request.user  # Logged-in user
    context = {
        'user': user
    }
    return render(request, 'banking/virtual_card.html', context)


def branch_finder(request):
    query = request.GET.get('q', '')  # user searches by city or IFSC
    branches = []

    if query:
        branches = CustomUser.objects.filter(
            Q(city__icontains=query) | Q(ifsc_code__icontains=query)
        ).values('city', 'ifsc_code')

    return render(request, 'banking/branch_finder.html', {'branches': branches, 'query': query})