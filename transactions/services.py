from fileinput import lineno
from .models import Transaction
from users.models import User
from wallet.models import Wallet
from django.db import transaction as db_transaction
from decimal import Decimal
import logging
transactions_logger = logging.getLogger("transactions_logger")

def send_money_service(sender_ac_no,reciver_ac_no,amount,password):
   
    
    try:
        sender  = User.objects.get(account_number=sender_ac_no)
        reciver = User.objects.get(account_number=reciver_ac_no)
        if reciver.account_number == sender.account_number:
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Sender and Receiver cannot be the same.")
            return {"success": False, "message": "Sender and Receiver cannot be the same."}
        if reciver.role != 'customer':
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Reciver is not a valid customer.")
            return {"success": False, "message": "Receiver is not a valid customer."}
        if not sender.check_password(password):
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Invalid Password.")
            return {"success": False, "message": "Invalid password."}
    except User.DoesNotExist:
        transactions_logger.error(
    f"[{lineno}]FAILED Transaction — User Does Not Exist"
)
        return {"success": False, "message": "Sender or Receiver does not exist."}
    transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
    
    sender_wallet = sender.wallet
    reciver_wallet = reciver.wallet
    amount = Decimal(amount)
    with db_transaction.atomic():
        if sender.wallet.balance < amount:
            transaction = Transaction.objects.create(
                
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='failed',
                transaction_type='sendmoney',
            )
            transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
            return {"success": False, "message": "Insufficient balance."}
        else:
            sender.wallet.balance -= amount
            reciver.wallet.balance += amount
            sender.wallet.save()
            reciver.wallet.save()
            transaction = Transaction.objects.create(
                
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='completed',
                transaction_type='sendmoney',
            )
            transactions_logger.info(f"[{lineno}] Sucessful transaction: from {sender.account_number} to {reciver.account_number} amount: {amount} transaction_id: {transaction.transaction_id}")
            return {"success": True, "message": "Transaction completed successfully.", "transaction_id": transaction.transaction_id}


def cashin_service(sender_ac_no,reciver_ac_no,amount):
   
    
    try:
        sender  = User.objects.get(account_number=sender_ac_no)
        reciver = User.objects.get(account_number=reciver_ac_no)
        if reciver.account_number == sender.account_number:
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Sender and Receiver cannot be the same.")
            return {"success": False, "message": "Sender and Receiver cannot be the same."}
        if reciver.role != 'customer':
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Reciver is not a valid customer.")
            return {"success": False, "message": "Receiver is not a valid customer."}
    except User.DoesNotExist:
        transactions_logger.error(
    f"[{lineno}]FAILED Transaction — User Does Not Exist"
)
        return {"success": False, "message": "Sender or Receiver does not exist."}
    transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
    
    sender_wallet = sender.wallet
    reciver_wallet = reciver.wallet
    amount = Decimal(amount)
    with db_transaction.atomic():
        if sender.wallet.balance < amount:
            transaction = Transaction.objects.create(
                
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='failed',
                transaction_type='cashin',
            )
            transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
            return {"success": False, "message": "Insufficient balance."}
        else:
            sender.wallet.balance -= amount
            reciver.wallet.balance += amount
            sender.wallet.save()
            reciver.wallet.save()
            transaction = Transaction.objects.create(
                
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='completed',
                transaction_type='cashin',
            )
            transactions_logger.info(f"[{lineno}] Sucessful transaction: from {sender.account_number} to {reciver.account_number} amount: {amount} transaction_id: {transaction.transaction_id}")
            return {"success": True, "message": "Transaction completed successfully.", "transaction_id": transaction.transaction_id}



def cash_out_service(sender_ac_no,agent_ac_no,amount):
     
    try:
        sender  = User.objects.get(account_number=sender_ac_no)
        reciver = User.objects.get(account_number=agent_ac_no)
        if reciver.role != 'agent':
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Reciver is not a valid agent.")
            return {"success": False, "message": "Receiver is not a valid agent."}
            
    except User.DoesNotExist:
        transactions_logger.error(f"[{lineno}]FAILED Transaction — User Does Not Exist")
        return {"success": False, "message": "Sender or Receiver does not exist."}
    transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
    sender_wallet = sender.wallet
    reciver_wallet = reciver.wallet
    amount = Decimal(amount)
    with db_transaction.atomic():
        if sender.wallet.balance < amount:
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='failed',
                transaction_type='cashout',
                
            )
            transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
            return {"success": False, "message": "Insufficient balance."}
        else:
            sender.wallet.balance -= amount
            reciver.wallet.balance += amount
            sender.wallet.save()
            reciver.wallet.save()
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='completed',
                transaction_type='cashout',
            )
            transactions_logger.info(f"[{lineno}] Sucessful transaction: from {sender.account_number} to {reciver.account_number} amount: {amount} transaction_id: {transaction.transaction_id}")
            return {"success": True, "message": "Transaction completed successfully.", "transaction_id": transaction.transaction_id}


def payment_service(sender_ac_no,merchant_ac_no,amount):
     
    try:
        sender  = User.objects.get(account_number=sender_ac_no)
        reciver = User.objects.get(account_number=merchant_ac_no)
        if reciver.role != 'merchant':
            transactions_logger.error(f"[{lineno}]FAILED Transaction — Reciver is not a valid merchant.")
            return {"success": False, "message": "Receiver is not a valid merchant."}
            
    except User.DoesNotExist:
        transactions_logger.error(f"[{lineno}]FAILED Transaction — User Does Not Exist")
        return {"success": False, "message": "Sender or Receiver does not exist."}
    transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
    sender_wallet = sender.wallet
    reciver_wallet = reciver.wallet
    amount = Decimal(amount)
    with db_transaction.atomic():
        if sender.wallet.balance < amount:
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='failed',
                transaction_type='payment'
            )
            transactions_logger.error(
    f"[{lineno}]FAILED Transaction — Insufficient Balance"
    )
            return {"success": False, "message": "Insufficient balance."}
        else:
            sender.wallet.balance -= amount
            reciver.wallet.balance += amount
            sender.wallet.save()
            reciver.wallet.save()
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=reciver,
                sender_wallet=sender_wallet,
                receiver_wallet=reciver_wallet,
                amount=amount,
                status='completed',
                transaction_type='payment'
            )
            transactions_logger.info(f"[{lineno}] Sucessful transaction: from {sender.account_number} to {reciver.account_number} amount: {amount} transaction_id: {transaction.transaction_id}")
            return {"success": True, "message": "Transaction completed successfully.", "transaction_id": transaction.transaction_id}
def transaction_history_service(user_ac_no):
    # try:
    #     user = User.objects.get(account_number=user_ac_no)
    # except User.DoesNotExist:
    #     transactions_logger.error(f"User with account number {user_ac_no} does not exist.")
    #     return {"success": False, "message": "User does not exist."}
    trx_history = Transaction.objects.filter(sender__account_number=user_ac_no).order_by('-transaction_time')[:10] | Transaction.objects.filter(receiver__account_number=user_ac_no).order_by('-transaction_time')[:10]
    history_list = []
    for trx in trx_history:
        history_list.append({
            "transaction_id": trx.transaction_id,
            "sender": trx.sender.account_number,
            "receiver": trx.receiver.account_number,
            "amount": str(trx.amount),
            "transaction_type": trx.transaction_type,
            "transaction_time": trx.transaction_time,
            "status": trx.status,
        })
    return {"success": True, "transaction_history": history_list}
