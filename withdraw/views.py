from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.views.decorators.csrf import csrf_exempt

from withdraw.forms import WithdrawForm
# Create your views here.


@login_required
@csrf_exempt
def withdrawForm(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = WithdrawForm()
    return render(request, 'withdraw/withdraw_form.html', {'form': form})


@login_required
@csrf_exempt
def proceessWithdraw(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'withdraw/process_withdraw.html')