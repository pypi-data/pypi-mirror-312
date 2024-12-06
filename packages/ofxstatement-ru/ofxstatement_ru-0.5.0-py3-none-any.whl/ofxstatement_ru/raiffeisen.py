# Raiffeisen Bank CSV plugin for ofxstatement

import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable, Optional, TextIO

from ofxstatement.parser import StatementParser, AbstractStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import (
    Statement,
    StatementLine,
    generate_transaction_id,
    Currency,
)

# Дата транзакции   Описание	Валюта операции	Сумма в валюте операции	Валюта счета	Сумма в валюте счета
# 25.09.2024 00:00

# file format options
t_delimiter = ";"
t_time_format = "%d.%m.%Y %H:%M"
t_encoding = "cp1251"
t_fieldnames = [
    "tr_time",
    "description",
    "op_currency",
    "op_amount",
    "currency",
    "amount",
]


def parse_type(type: str, amount: Decimal) -> Optional[str]:
    result = None

    if amount > 0:
        result = "DEBIT"
    elif amount < 0:
        result = "CREDIT"

    return result


class RaiffeiseStatementParser(StatementParser):
    statement: Statement

    def __init__(self, fin: "TextIO"):
        super().__init__()
        self.statement = Statement()
        self.fin = fin
        # Skip 1st row with column's headers
        self.fin.readline()
        self.cur_record = 1

    def split_records(self) -> Iterable[StatementLine]:
        return csv.DictReader(self.fin, delimiter=t_delimiter, fieldnames=t_fieldnames)

    def parse_record(self, line: StatementLine) -> Optional[StatementLine]:
        transaction = StatementLine()

        op_amount: Decimal
        try:
            op_amount = Decimal(line["op_amount"].replace(" ", ""))
        except InvalidOperation:
            print(
                "Error: Skipping line %d: Transaction time %s op_amount is not a number."
                % (self.cur_record, line["tr_time"])
            )
            return None

        amount = Decimal(line["amount"].replace(" ", ""))

        if not line["currency"] == self.statement.currency:
            print(
                "Transaction %s currency '%s' differ from account currency '%s'."
                % (line["tr_time"], line["currency"], self.statement.currency)
            )
            return None

        transaction.currency = Currency(line["currency"], Decimal(1))
        rate = Decimal(amount / op_amount)
        transaction.orig_currency = Currency(line["op_currency"], rate)

        transaction.date = datetime.strptime(line["tr_time"], t_time_format)

        transaction.amount = amount

        transaction.trntype = parse_type(line["description"], transaction.amount)

        transaction.memo = line["description"]

        # as csv file does not contain explicit id of transaction, generating artificial one
        transaction.id = generate_transaction_id(transaction)

        if transaction.trntype:
            return transaction
        else:
            return None


class RaiffeisenPlugin(Plugin):
    """Raiffeisen Bank CSV (http://raiffeisen.ru)"""

    def get_parser(self, filename: str) -> AbstractStatementParser:
        f = open(filename, "r", encoding=t_encoding)
        parser = RaiffeiseStatementParser(f)
        parser.statement.account_id = self.settings["account"]
        parser.statement.bank_id = self.settings.get("bank", "Raiffeisen")
        parser.statement.currency = self.settings.get("currency", "RUB")
        return parser
