import pdfplumber
import re
from utils.text_utils import merge_lines

def parse_bob(file):

    data = []
    seen = set()

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if table:
                # USE TABLE ONLY
                for row in table[1:]:  # skip header

                    try:
                        if not row or len(row) < 5:
                            continue

                        date = row[0]

                        # adjust index if needed
                        debit = row[4]
                        credit = row[5]
                        desc = row[1]

                        debit_val = float(str(debit).replace(",", "")) if debit else 0

                        #  ONLY DEBIT
                        if debit_val <= 0:
                            continue

                        desc = re.sub(r'[^a-zA-Z ]', ' ', str(desc)).strip().lower()

                        key = f"{date}-{debit_val}-{desc}"
                        if key in seen:
                            continue
                        seen.add(key)

                        data.append({
                            "date": date,
                            "description": desc,
                            "amount": debit_val
                        })

                    except:
                        continue

            else:
                #  FALLBACK TO TEXT ONLY IF NO TABLE
                text = page.extract_text()
                if not text:
                    continue

                lines = text.split("\n")
                merged_lines = merge_lines(lines)

                for line in merged_lines:

                    if not re.match(r"\d{2}/\d{2}/\d{4}", line):
                        continue

                    try:
                        amounts = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

                        if len(amounts) < 2:
                            continue

                        debit = float(amounts[0].replace(",", ""))
                        credit = float(amounts[1].replace(",", ""))

                        # ONLY DEBIT
                        if debit <= 0:
                            continue

                        desc = re.sub(r"\d{1,3}(?:,\d{3})*\.\d{2}", "", line)
                        desc = re.sub(r"\d{2}/\d{2}/\d{4}", "", desc)
                        desc = re.sub(r'[^a-zA-Z ]', ' ', desc)
                        desc = desc.strip().lower()

                        key = f"{line[:10]}-{debit}-{desc}"
                        if key in seen:
                            continue
                        seen.add(key)

                        data.append({
                            "date": line[:10],
                            "description": desc,
                            "amount": debit
                        })

                    except:
                        continue

    print("TOTAL PARSED:", len(data))
    print("TOTAL:", sum([t["amount"] for t in data]))
    print("SAMPLE DATA:", data[:5])

    return data