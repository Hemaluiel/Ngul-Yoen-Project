def normalize_transaction(date, desc, debit, credit):

    debit = float(debit or 0)
    credit = float(credit or 0)

    if debit > 0:
        return {
            "date": date,
            "description": desc,
            "debit": debit,
            "credit": 0.0,
            "amount": debit,
            "type": "debit"
        }

    if credit > 0:
        return {
            "date": date,
            "description": desc,
            "debit": 0.0,
            "credit": credit,
            "amount": credit,
            "type": "credit"
        }

    return None