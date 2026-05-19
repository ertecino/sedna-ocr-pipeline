import pandas as pd
from pathlib import Path
from .models import WaybillData

def save_to_csv(data: WaybillData, output_path: str | Path):
    """
    Flattens the WaybillData and exports it to a Sedna-compatible CSV file.
    """
    rows = []

    for item in data.items:
        row = {
            "Tarih": data.document_date,
            "Fis_No": data.document_number,
            "Cari_Hesap": data.supplier_name,
            "Malzeme_Adi": item.product_name,
            "Miktar": item.quantity,
            "Birim": item.unit,
            "Birim_Fiyat": item.unit_price
        }
        rows.append(row)

    if not rows:
        # If no items, we still might want to write an empty CSV with headers,
        # or just skip. We will create an empty DataFrame with the required columns.
        df = pd.DataFrame(columns=[
            "Tarih", "Fis_No", "Cari_Hesap", "Malzeme_Adi", "Miktar", "Birim", "Birim_Fiyat"
        ])
    else:
        df = pd.DataFrame(rows)

    # Sedna requires semicolon separator
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
    return output_path
