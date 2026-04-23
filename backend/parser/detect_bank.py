def detect_bank(text):
    text = text.lower()

    if "bank of bhutan" in text:
        return "BOB"
    elif "bhutan national bank" in text:
        return "BNB"
    elif "t-bank" in text or "tbank" in text:
        return "TBANK"
    else:
        return "UNKNOWN"