from pydantic import BaseModel, Field
from typing import List, Optional

class Item(BaseModel):
    product_name: str = Field(description="Malzeme Adı (Product Name)")
    quantity: float = Field(description="Miktar (Quantity)")
    unit: str = Field(description="Birim (Unit - e.g., KG, ADET)")
    unit_price: float = Field(description="Birim Fiyat (Unit Price)")

class WaybillData(BaseModel):
    document_date: str = Field(description="Tarih - Format: DD.MM.YYYY")
    document_number: str = Field(description="İrsaliye/Fatura No (Document Number)")
    supplier_name: str = Field(description="Tedarikçi Adı (Supplier Name)")
    items: List[Item] = Field(description="List of products")
