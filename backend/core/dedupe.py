def dedupe(transactions):
    seen = set()
    clean = []

    for t in transactions:
        key = f"{t['date']}-{t['amount']}-{t['description']}"

        if key not in seen:
            seen.add(key)
            clean.append(t)

    return clean