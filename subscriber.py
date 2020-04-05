import time
import datetime
import json
import redis
from peewee import PostgresqlDatabase, Model, CharField, BooleanField, IntegerField, SmallIntegerField, DateTimeField

# Connect to a Postgres database.
db = PostgresqlDatabase('postgres', user='postgres', password='secret', 
                        host='db', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Transaction(BaseModel):
    transaction_id = CharField(unique=True)
    transaction_account = CharField()
    transaction_time = DateTimeField()
    description = CharField()
    mcc = SmallIntegerField()
    hold = BooleanField(default=False)
    amount = IntegerField()
    operationAmount = IntegerField()
    currencyCode = SmallIntegerField()
    commissionRate = SmallIntegerField()
    cashbackAmount = IntegerField()
    balance = IntegerField()

db.create_tables([Transaction])

client = redis.Redis(host='redis', port=6379, db=0)
pubsub = client.pubsub()
pubsub.subscribe('transactions')

while True:
    message = pubsub.get_message()
    if message:
        if message['type'] == 'message':
            transaction = json.loads(message['data'])
            Transaction.create(
                transaction_id=transaction['data']['statementItem'].get('id'),
                transaction_account=transaction['data'].get('account'),
                transaction_time=datetime.datetime.fromtimestamp(transaction['data']['statementItem'].get('time')),
                description=transaction['data']['statementItem'].get('description'),
                mcc=transaction['data']['statementItem'].get('mcc'),
                hold=transaction['data']['statementItem'].get('hold'),
                amount=transaction['data']['statementItem'].get('amount'),
                operationAmount=transaction['data']['statementItem'].get('operationAmount'),
                currencyCode=transaction['data']['statementItem'].get('currencyCode'),
                commissionRate=transaction['data']['statementItem'].get('commissionRate'),
                cashbackAmount=transaction['data']['statementItem'].get('cashbackAmount'),
                balance=transaction['data']['statementItem'].get('balance')
            )
    time.sleep(1)
