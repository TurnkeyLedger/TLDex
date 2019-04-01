from django import forms

from deposit.models import DepositModel

FIAT_CURRENCIES_CHOICES = (
    ('usd', 'USD'),
    ('eur', 'EUR'),
    ('tnd', 'TND'),
)

CRYPTO_CURRENCIES_CHOICES = (
    ('btc', 'BTC'),
    ('eth', 'ETH'),
    ('bass', 'BASS'),
)

class DepositForm(forms.ModelForm):

    class Meta:
        model = DepositModel
        fields = ['amount','fiat_Currency','crypto_Address']





