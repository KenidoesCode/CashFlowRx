import pdfplumber
import pandas as pd
import re

def process(uploaded_pdf):
    rows = []
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            for line in (page.extract_text() or "").splitlines():
                m = re.search(r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?\d+\.?\d*)$', line)
                if m:
                    rows.append({
                        "date": m.group(1),
                        "description": m.group(2),
                        "amount": float(m.group(3))
                    })
    return pd.DataFrame(rows)
