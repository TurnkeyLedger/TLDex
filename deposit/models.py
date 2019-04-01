from datetime import datetime

from django.db import models

# Create your models here.


USD = 'USD'

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

class DepositModel(models.Model):
    transaction_id = models.CharField(default="", max_length=50, primary_key=True)
    custom = models.CharField(max_length=50,blank=True, null=True)
    amount = models.IntegerField(default=1)
    fiat_Currency = models.CharField(max_length=3, choices=FIAT_CURRENCIES_CHOICES, default=USD)
    crypto_Address = models.CharField(max_length=35)
    crypto_amount = models.FloatField(blank=True, null=True)
    success_boolean = models.BooleanField(blank=True, null=True)

    #user infos
    """first_name = models.CharField(default="",max_length=30)
    last_name = models.CharField(max_length=30)
    payer_email = models.EmailField()
    payer_status = models.CharField(max_length=30)
    residence_country = models.CharField(max_length=20)"""











