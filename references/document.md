# Document Mode

For receipts, invoices, bills, CVs/resumes, menus, price lists, forms, ID/business cards, contracts, certificates, tickets, slides.

Top-level shape (after `mode` + `_meta`):

```json
{
  "mode": "document",
  "_meta": { ... },
  "document_type": "...",
  "language": "...",
  "metadata": { ... },
  "parties": [ ... ],
  "sections": [ ... ],
  "tables": [ ... ],
  "key_values": { ... },
  "totals": { ... },
  "extracted_text": "...",
  "visual_state": { ... }
}
```

## document_type
Short label: `receipt` | `invoice` | `resume` | `menu` | `price_list` | `form` | `id_card` | `business_card` | `contract` | `certificate` | `ticket` | `slide` | `other`.

## language
Primary language detected, e.g. `"vi"`, `"en"`, `"mixed (vi/en)"`.

## metadata
Document-level fields; `null` for absent ones.
```json
"metadata": { "title": "INVOICE", "document_number": "INV-2026-0042", "issue_date": "2026-06-04", "due_date": "2026-06-18", "reference": "PO-9981", "page": "1/1" }
```

## parties
Array of people/organizations. Flexible roles — `seller`, `buyer`, `candidate`, `employer`, `issuer`, `passenger`, `landlord`, `tenant`, etc.
```json
"parties": [ { "role": "seller", "name": "ACME Coffee Co.", "address": "12 Le Loi, District 1, HCMC", "tax_id": "0312345678", "phone": "+84 28 1234 5678", "email": "billing@acme.example" } ]
```

## sections
Ordered logical blocks (header, contact, work experience, terms, notes…). Use for free-form content like a CV.
```json
"sections": [ { "id": "work_experience", "heading": "Work Experience", "content": "Senior Developer at FPT (2022–2026)…", "items": ["Senior Developer — FPT (2022–2026)", "Developer — VNG (2019–2022)"] } ]
```
`items` optional — bullet/list content, else `[]`.

## tables
Each table keeps header + rows. Cell values are strings exactly as printed (keep currency symbols, separators, units).
```json
"tables": [ { "id": "line_items", "caption": "Order Items", "columns": ["Item", "Qty", "Unit Price", "Amount"], "rows": [ ["Cappuccino", "2", "55,000", "110,000"], ["Croissant", "1", "40,000", "40,000"] ] } ]
```
Merged cells (`colspan`/`rowspan`): duplicate the value across spanned positions or fill `""` to keep every row's column count consistent.

## key_values
Flat label→value map for fields that don't fit elsewhere (great for forms/cards).
```json
"key_values": { "Cashier": "Linh", "Table": "12", "Payment Method": "Cash" }
```

## totals
Monetary/numeric summary; custom taxes/charges as extra keys or in `key_values`.
```json
"totals": { "subtotal": "150,000", "discount": "0", "tax": "15,000", "shipping": null, "grand_total": "165,000", "currency": "VND", "amount_in_words": "One hundred sixty-five thousand dong" }
```

## extracted_text
Full raw OCR of the document as one string, line breaks as `\n`. The lossless safety net — always populate it.

## visual_state
```json
"visual_state": { "orientation": "portrait", "quality": "clear", "is_handwritten": false, "has_logo": true, "has_signature": false, "has_stamp": false, "special_notes": null }
```
`quality`: `clear` | `slightly blurry` | `low-res` | `partially obscured`.

## Rules

1. Output ONLY the raw JSON.
2. Transcribe text exactly as printed; don't translate, reformat numbers, or "fix" values unless asked.
3. Absent field → `null`; empty array → `[]`.
4. Always populate `extracted_text` even when structured fields are filled.
5. Unreadable characters → `"[illegible]"` inline within the value.
6. Never add comments inside the JSON.

## Handling uncertain values (fallback)

When a high-stakes value is printed but hard to read (faded ink, glare, smudge), don't silently guess and don't drop it — wrap just that value with field-level confidence so the consumer knows to double-check it. Everything clearly legible stays a plain string.

```json
{
  "mode": "document",
  "_meta": { "schema_version": "1.0.1", "source": "photo", "image_orientation": "portrait", "detected_language": "vi", "confidence": "medium", "notes": "Receipt total partly smudged" },
  "document_type": "receipt",
  "language": "vi",
  "metadata": { "title": "HÓA ĐƠN", "document_number": "HD-2026-0510", "issue_date": "2026-06-04", "due_date": null, "reference": null, "page": "1/1" },
  "parties": [],
  "sections": [],
  "tables": [],
  "key_values": { "Hình thức thanh toán": "Tiền mặt" },
  "totals": {
    "subtotal": "180,000",
    "discount": "0",
    "tax": "18,000",
    "shipping": null,
    "grand_total": { "value": "198,000", "confidence": "low", "reason": "last digit smudged, could be 198,000 or 199,000" },
    "currency": "VND",
    "amount_in_words": null
  },
  "extracted_text": "HÓA ĐƠN\nSố: HD-2026-0510\nNgày: 2026-06-04\nCộng tiền hàng: 180,000\nVAT 10%: 18,000\nTổng cộng: 19[8/9],000\nThanh toán: Tiền mặt",
  "visual_state": { "orientation": "portrait", "quality": "partially obscured", "is_handwritten": false, "has_logo": false, "has_signature": false, "has_stamp": false, "special_notes": "grand total digit ambiguous" }
}
```

---

## Worked Example

Below is a complete, fully valid JSON output representing a printed coffee shop receipt document:

```json
{
  "mode": "document",
  "_meta": {
    "schema_version": "1.0.1",
    "source": "scan",
    "image_orientation": "portrait",
    "detected_language": "vi",
    "confidence": "high",
    "notes": "Hóa đơn thanh toán cà phê"
  },
  "document_type": "receipt",
  "language": "vi",
  "metadata": {
    "title": "HÓA ĐƠN BÁN HÀNG",
    "document_number": "HD-2026-0089",
    "issue_date": "2026-06-04",
    "due_date": null,
    "reference": "Bàn số 5",
    "page": "1/1"
  },
  "parties": [
    {
      "role": "seller",
      "name": "CÀ PHÊ SÀI GÒN",
      "address": "45 Nguyễn Huệ, Quận 1, TP. HCM",
      "tax_id": "0311223344",
      "phone": "+84 28 3822 1100",
      "email": "contact@caphesaigon.vn"
    }
  ],
  "sections": [],
  "tables": [
    {
      "id": "mat_hang",
      "caption": "Chi tiết hóa đơn",
      "columns": ["STT", "Tên món", "SL", "Đơn giá", "Thành tiền"],
      "rows": [
        ["1", "Cà phê sữa đá", "2", "35,000", "70,000"],
        ["2", "Bánh mì pate", "1", "45,000", "45,000"]
      ]
    }
  ],
  "key_values": {
    "Thu ngân": "Nguyễn Thị Hoa",
    "Hình thức thanh toán": "MOMO"
  },
  "totals": {
    "subtotal": "115,000",
    "discount": "0",
    "tax": "11,500",
    "shipping": null,
    "grand_total": "126,500",
    "currency": "VND",
    "amount_in_words": "Một trăm hai mươi sáu ngàn năm trăm đồng"
  },
  "extracted_text": "CÀ PHÊ SÀI GÒN\nĐịa chỉ: 45 Nguyễn Huệ, Quận 1, TP. HCM\nTax ID: 0311223344\n\nHÓA ĐƠN BÁN HÀNG\nSố: HD-2026-0089\nNgày: 2026-06-04\n\nBàn số 5\n\n1. Cà phê sữa đá | SL: 2 | Đơn giá: 35,000 | Thành tiền: 70,000\n2. Bánh mì pate | SL: 1 | Đơn giá: 45,000 | Thành tiền: 45,000\n\nCộng tiền hàng: 115,000\nThuế VAT (10%): 11,500\nTổng cộng thanh toán: 126,500\n\nThu ngân: Nguyễn Thị Hoa\nThanh toán: MOMO\nCảm ơn quý khách!",
  "visual_state": {
    "orientation": "portrait",
    "quality": "clear",
    "is_handwritten": false,
    "has_logo": true,
    "has_signature": false,
    "has_stamp": false,
    "special_notes": null
  }
}
```

