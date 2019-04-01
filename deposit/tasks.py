# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from .ServicesBITCOIN import ServiceBitcoin




"""
PENDING (waiting for execution or unknown task id)
STARTED (task has been started)
SUCCESS (task executed successfully)
FAILURE (task execution resulted in exception)
RETRY (task is being retried)
REVOKED (task has been revoked)
"""

logger=get_task_logger(__name__)

@shared_task(name='deposit.tasks.bitcoinpayment')
def serviceBITCOINTask(receiverAddress, amountToSend):
    logger.info("perform bitcoin tansaction")
    return ServiceBitcoin(receiverAddress, amountToSend).main()






