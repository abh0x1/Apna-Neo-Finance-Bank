from django import forms

TRANSACTION_MODES = [
    ('IMPS', 'IMPS'),
    ('RTGS', 'RTGS'),
    ('NEFT', 'NEFT'),
    ('UPI', 'UPI'),
]

TRANSFER_BY_CHOICES = [
    ('username', 'Username'),
    ('account_number', 'Account Number'),
    ('mobile', 'Mobile Number'),
    ('upi', 'UPI ID'),
]

class FundTransferForm(forms.Form):
    transfer_by = forms.ChoiceField(label="Send To", choices=TRANSFER_BY_CHOICES)
    receiver_value = forms.CharField(label="Receiver Info")  # depending on choice
    amount = forms.DecimalField(label="Amount", max_digits=12, decimal_places=2)
    transaction_mode = forms.ChoiceField(label="Transfer Mode", choices=TRANSACTION_MODES)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)
