from django.shortcuts import render
from django.conf import settings



url_ngrok = settings.ALLOWED_URL_NGROK

def index(request):
    context = {'url_ngrok': url_ngrok}

    return render(request,'index.html',context)

def news(request):
    return render(request,'news.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def wallet(request):
    return render(request,'wallet.html')


def get_coins_price(request):
    btc_coin = request.GET.get('btc_coin')
    eth_coin = request.GET.get('eth_coin')
    btc_coin = request.GET.get('btc_coin')
    btc_coin = request.GET.get('btc_coin')
    btc_coin = request.GET.get('btc_coin')