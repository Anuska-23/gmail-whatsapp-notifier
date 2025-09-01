from email.header import decode_header, make_header

def decode_mime_header(raw):
    if raw is None:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw

def make_snippet(text, max_len=200):
    if not text:
        return ""
    text = " ".join(text.split())
    return (text[: max_len - 1] + "…") if len(text) > max_len else text
