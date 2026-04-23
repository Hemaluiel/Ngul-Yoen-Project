import re

def merge_lines(lines):
    merged = []
    current = ""

    for line in lines:
        line = line.strip()

        # new transaction starts with date
        if re.match(r"\d{2}/\d{2}/\d{4}", line):
            if current:
                merged.append(current)
            current = line
        else:
            current += " " + line

    if current:
        merged.append(current)

    return merged