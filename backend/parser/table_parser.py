import pdfplumber
from core.normalize import normalize_transaction

def parse_table(file):

    transactions = []

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if not table:
                continue

            for row in table[1:]:

                try:
                    date = row[0]
                    desc = row[1]
                    debit = row[-2]
                    credit = row[-1]

                    tx = normalize_transaction(date, desc, debit, credit)

                    if tx:
                        transactions.append(tx)

                except:
                    continue

    return transactions