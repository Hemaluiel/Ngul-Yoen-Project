import pdfplumber

def parse_bnb(pdf_file):
    data = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if not table:
                continue

            for row in table[1:]:
                try:
                    date = row[0]
                    description = row[2]
                    withdrawal = row[3]   # BNB may use different column index

                    if withdrawal and float(withdrawal) > 0:
                        data.append({
                            "date": date,
                            "description": description,
                            "amount": float(withdrawal),
                            "type": "debit"
                        })

                except:
                    continue

    return data