def dedupe(transactions):

    seen = set()
    clean = []

    for t in transactions:

        key = (t["date"], t["description"], t["amount"], t["type"])

        if key in seen:
            continue

        seen.add(key)
        clean.append(t)

    return clean