import pdfplumber

def parse_bob(pdf_file):
    data = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()

            if not table:
                continue

            # Detect headers dynamically
            headers = [str(h).lower() if h else "" for h in table[0]]

            try:
                date_idx = next(i for i, h in enumerate(headers) if "date" in h)
                desc_idx = next(i for i, h in enumerate(headers) if "description" in h or "details" in h)
                debit_idx = next(i for i, h in enumerate(headers) if "debit" in h or "withdrawal" in h)
            except StopIteration:
                continue  # skip if structure not recognized

            for row in table:
                # Skip empty or header rows
                if not row or "date" in str(row).lower():
                    continue

                try:
                    date = row[date_idx]
                    description = row[desc_idx]
                    debit = row[debit_idx]

                    if not debit or debit.strip() == "":
                        continue

                    amount = float(debit.replace(",", ""))

                    if amount > 0:
                        data.append({
                            "date": date,
                            "description": description,
                            "amount": amount,
                            "type": "debit"
                        })

                except:
                    continue

    return data