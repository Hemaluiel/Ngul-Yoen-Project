import pdfplumber
import re

def clean_text(x):
    if not x:
        return ""
    x = re.sub(r"[^a-zA-Z ]", " ", str(x))
    return re.sub(r"\s+", " ", x).strip()


def safe_float(x):
    try:
        return float(x.replace(",", ""))
    except:
        return 0.0


def parse_universal(file):

    transactions = []
    seen = set()

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            table = page.extract_table()


            # 1. TABLE PARSING - PRIORITY

            if table:

                for row in table[1:]:

                    if not row or len(row) < 4:
                        continue

                    try:
                        date = row[0]
                        desc = clean_text(row[1])

                        # try safe column guessing
                        debit = safe_float(row[-2])
                        credit = safe_float(row[-1])

                        # ONLY DEBIT IS EXPENSE
                        if debit > 0:
                            amount = debit
                        else:
                            continue  
                        # if debit <= 0:
                        #     continue

                        key = f"{date}-{debit}-{desc}"
                        if key in seen:
                            continue
                        seen.add(key)

                        transactions.append({
                            "date": date,
                            "description": desc,
                            "amount": debit
                        })

                    except:
                        continue


            # 2. TEXT FALLBACK -ONLY IF NO TABLE

            else:

                text = page.extract_text()
                if not text:
                    continue

                for line in text.split("\n"):

                    if not re.match(r"\d{2}/\d{2}/\d{4}", line):
                        continue

                    amounts = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                    if len(amounts) < 1:
                        continue

                    debit = safe_float(amounts[0])

                    # if debit <= 0:
                    #     continue
                    if debit > 0:
                        amount = debit
                    else:
                        continue  

                    desc = clean_text(line)

                    key = f"{line[:10]}-{debit}-{desc}"
                    if key in seen:
                        continue
                    seen.add(key)

                    transactions.append({
                        "date": line[:10],
                        "description": desc,
                        "amount": debit
                    })

    print("TOTAL PARSED:", len(transactions))
    return transactions