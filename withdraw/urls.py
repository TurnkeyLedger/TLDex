from django.urls import path
from withdraw.views import withdrawForm,proceessWithdraw

app_name = 'withdraw'

urlpatterns = [
    path('sell/', withdrawForm, name='sell'),
    path('process/', proceessWithdraw, name='process'),
    ]