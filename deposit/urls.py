from django.urls import path
from deposit.views import processFiatPayment, deposit,depositComplete,depositCancelled,depositOnProgress,paypalResponse,get_task_info,get_coins_price

app_name = 'deposit'

urlpatterns = [
    path('buy/', deposit, name='buy'),
    path('process/', processFiatPayment, name='processdeposit'),
    path('done/', depositComplete, name='done'),
    path('cancelled/', depositCancelled, name='cancelled'),
    path('onprogress/', depositOnProgress, name='onprogress'),
    path('notify/',paypalResponse,name='notify'),
    path('gettaskinfo/', get_task_info,name='gettaskinfo'),
    path('getprice/', get_coins_price,name='getprice'),


    ]