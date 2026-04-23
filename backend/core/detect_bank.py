def detect_bank(text):
    text = text.lower()

    if "bank of bhutan" in text:
        return "BOB"
    elif "bhutan national bank" in text or "bnb" in text:
        return "BNB"
    elif "druk bank" in text or "dk bank" in text:
        return "DK"
    else:
        return "UNKNOWN"