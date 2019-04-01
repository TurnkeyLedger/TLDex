from django import forms

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

PAYMRNT_OPTIONS_CHOICES = (
    ('paypal', 'PAYPAL'),
    ('bastoji', 'BASTOJI'),
)

class WithdrawForm(forms.Form):

    amount = forms.IntegerField(required=True,initial=1,min_value=1,max_value=999, label="Amount",)
    fiat_Curency = forms.MultipleChoiceField(required=True,
                                           widget=forms.Select,
                                           choices=FIAT_CURRENCIES_CHOICES, )

    payment_Options = forms.MultipleChoiceField(required=True,
                                             widget=forms.Select,
                                             choices=PAYMRNT_OPTIONS_CHOICES, )
    address = forms.EmailField(required=True)