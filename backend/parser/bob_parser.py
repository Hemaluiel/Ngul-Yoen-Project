import pdfplumber

def parse_bob(pdf_file):
    data = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if not table:
                continue

            for row in table[1:]:
                try:
                    date = row[0]
                    description = row[1]
                    debit = row[2]
                    credit = row[3]

                    if debit and float(debit) > 0:
                        data.append({
                            "date": date,
                            "description": description,
                            "amount": float(debit),
                            "type": "debit"
                        })

                except:
                    continue

    return data