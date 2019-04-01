import json
from random import *
from celery import uuid
from celery.result import AsyncResult
from coinbase.wallet.client import Client
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# paypal import
from paypal.standard.forms import PayPalPaymentsForm

from deposit.models import DepositModel
from deposit.tasks import serviceBITCOINTask
from .forms import DepositForm

COINBASE_API_KEY = 'vnFfW3kq1R3MpC81'
COINBASE_API_SECRET = 'VdHevQp9hwmUMHtrBZdMM6cXYVkNPsmV'

# TODO create two function one handel the paypal payment process and the second handel the stripe or the braintree payment gateway {process_paypal_payment, process_stripe_payment}
# TODO test if the method is post if yes test for rerquest_id{paypal ,stripe}


Order = 'item'

rpcPort = 7233
rpcUser = 'rpc'
rpcPassword = 'rpc'
rpcIpAddress = '173.249.24.81'
receiverAddress = 'jucZiqUrTKp8z134C3XxamFq8DZPbdrCNh'
amountToSend = 0.08440000
serverRpcURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

serverWebURL = 'http://localhost:8000/payment-done/'

transactionID = uuid()


# model to save transaction a custom values to DB


@login_required
@csrf_protect
def processFiatPayment(request):
    if request.method == "POST":
        depositModel = DepositModel()
        # form to render transaction infos
        form = DepositForm(request.POST)

        if form.is_valid():
            """
            transaction_id = models.CharField(default="", max_length=50, primary_key=True)
            custom = models.CharField(max_length=50,blank=True, null=True)
            amount = models.IntegerField(blank=True, null=True)
            fiat_Currency = models.CharField(max_length=3, choices=FIAT_CURRENCIES_CHOICES, default=USD)
            crypto_Address = models.CharField(max_length=35)
            crypto_amout = models.FloatField(blank=True, null=True)
            success_boolean = models.BooleanField(blank=True, null=True)
            """

            # variable multi use
            host = request.get_host()
            custom = request.user.username
            amount = request.POST.get('amount')
            currency_code = form.cleaned_data.get('fiat_Currency').upper()
            currency_amount = calculateHowMuchBitcoin(amount, currency_code)

            # save values to DB

            depositModel.transaction_id = transactionID
            depositModel.custom = custom
            depositModel.amount = form.cleaned_data.get('amount')
            depositModel.fiat_Currency = form.cleaned_data.get('fiat_Currency')
            depositModel.crypto_Address = form.cleaned_data.get('crypto_Address')
            depositModel.crypto_amount = currency_amount
            depositModel.success_boolean = False

            depositModel.save()

            # paypal dict
            paypal_dict = {
                'actionType': 'PAY',
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': amount,
                'item_name': 'Buy BTC COIN',
                'txn_id': transactionID,
                'invoice': str(randint(1, 999)),
                'currency_code': currency_code,
                "custom": custom,
                'notify_url': 'http://{}{}'.format(host, reverse('deposit:notify')),
                'return_url': 'http://{}{}'.format(host, reverse('deposit:onprogress')),
                'cancel_return': 'http://{}{}'.format(host, reverse('deposit:cancelled')),
            }

            # display dict info
            infos_dict = {
                "custom": custom,
                'amount': amount,
                'currency_code': currency_code,
                "btc_amount": currency_amount
            }

            form = PayPalPaymentsForm(initial=paypal_dict)

            context = {"form": form,
                       "dicts": infos_dict}

            return render(request, 'deposit/process_deposit.html', context)

    else:

        form = DepositForm()
        return render(request, 'deposit/deposit_form.html', {'form': form})


@csrf_exempt
def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    print(task_id)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,

        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('No job id given.')

@login_required
@csrf_exempt
def depositOnProgress(request):
    url_ngrok = settings.ALLOWED_URL_NGROK

    dataTransaction = model_to_dict(DepositModel.objects.filter(Q(transaction_id=transactionID))[0])

    crypto_address = dataTransaction['crypto_Address']
    crypto_amount = dataTransaction['crypto_amount']


    send_bitcoin_task = serviceBITCOINTask.delay(crypto_address,crypto_amount)

    context = {
        'crypto_address': crypto_address,
        'crypto_amount': crypto_amount,
        'task_id': send_bitcoin_task.id,
        'url_ngrok': url_ngrok,
    }
    # print(context)
    return render(request, 'deposit/deposit_on_progress.html', context)


@login_required
@csrf_exempt
def depositComplete(request):
    return render(request, 'deposit/deposit_complete.html')


@login_required
@csrf_exempt
def depositCancelled(request):
    url_ngrok = settings.ALLOWED_URL_NGROK
    context  = {'url_ngrok':url_ngrok}
    return render(request, 'deposit/deposit_cancelled.html',context)

@login_required
@csrf_exempt
def deposit(request):
    form = DepositForm()
    return render(request, 'deposit/deposit_form.html', {'form': form})


@csrf_exempt
def paypalResponse(request):
    if request.method == 'POST':
        if request.POST.get('payment_status') == 'Completed':
            DepositModel.objects.filter(transaction_id=transactionID).update(success_boolean=True)

            return HttpResponse({'data':'ok'})
    else:
        return HttpResponse("Error")




"""def calculateHowMuchBitcoin(_fiatAmount,_currencyCode):
    client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
    currency_code = _currencyCode.upper()  # can also use EUR, CAD, etc.
    # Make the request
    sellprice = client.get_sell_price(currency_code=currency_code)
    amount = float(format(float(format(float(_fiatAmount), '.8f')) / float(format(float(sellprice.amount), '.8f')), '8f'))

    return str(amount)"""

@csrf_exempt
def get_coins_price(request):
    print('getprice')
    client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
    _currencyCode = request.GET.get('currencyCode',None)
    print(_currencyCode)
    if _currencyCode is not None:


        sellpricebtc= client.get_sell_price(currency_pair='BTC-{}'.format(_currencyCode.upper()))
        sellpriceeth = client.get_sell_price(currency_pair='ETH-{}'.format(_currencyCode.upper()))
        selpriceltc = client.get_sell_price(currency_pair='LTC-{}'.format(_currencyCode.upper()))
        selpricebch = client.get_sell_price(currency_pair='BCH-{}'.format(_currencyCode.upper()))
        sellpricebsv = client.get_sell_price(currency_pair='XRP-{}'.format(_currencyCode.upper()))
        context = {
            'btcprice':sellpricebtc,
            'ethprice':sellpriceeth,
            'ltcprice':selpriceltc,
            'bchprice':selpricebch,

        }

        print(context)

        return HttpResponse(json.dumps(context),content_type='application/json')
    else:
        return HttpResponse('get price error')


def calculateHowMuchBitcoin(_fiatAmount, _currencyCode):
    client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
    currency_code = _currencyCode.upper()  # can also use EUR, CAD, etc.
    # Make the request
    sellprice = client.get_sell_price(currency_code=currency_code)
    print(sellprice)
    _fiatAmountForFunc = float(_fiatAmount)
    _oneCoinPrice = float(sellprice.amount)

    _oneBTCInSatoshi = 100000000

    _oneSatoshiDollar = _oneCoinPrice / _oneBTCInSatoshi

    _oneDollarSatoshi = 1 / _oneSatoshiDollar

    btcAmount = round(round(_fiatAmountForFunc * _oneDollarSatoshi, 0) * 0.00000001, 8)

    return str(btcAmount)
