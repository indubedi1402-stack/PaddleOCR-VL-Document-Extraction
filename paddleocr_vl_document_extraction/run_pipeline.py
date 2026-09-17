import json
import re
from pathlib import Path

OCR_JSON = Path("output/invoice_res.json")
MARKDOWN = Path("output/invoice.md")
SCHEMA = Path("configs/extraction_schema.json")
FINAL = Path("output/final_result.json")

# Load files
data = json.loads(OCR_JSON.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
markdown = MARKDOWN.read_text(encoding="utf-8")

# PaddleOCR result is inside "res"
ocr = data["res"]

texts = ocr["rec_texts"]
boxes = ocr["dt_polys"]

patterns = {
    "invoice_number": r"Invoice Number:\s*(.+)",
    "date": r"Date:\s*(.+)",
    "vendor": r"Vendor:\s*(.+)",
    "customer": r"Customer:\s*(.+)",
    "total_amount": r"Total Amount:\s*(.+)"
}

result = {}

for field, field_type in schema.items():

    # Find value in Markdown
    match = re.search(patterns[field], markdown, re.IGNORECASE)

    if not match:
        result[field] = None
        continue

    value = re.sub(r"\*\*", "", match.group(1)).strip()

    if field_type == "number":
        value = float(re.sub(r"[^0-9.\-]", "", value))

    # Find matching OCR text for provenance
    provenance = None

    for i, text in enumerate(texts):
        if re.search(patterns[field], text, re.IGNORECASE):
            provenance = {
                "page": 1,
                "source_text": text,
                "bbox": boxes[i],
                "text_index": i
            }
            break

    result[field] = {
        "value": value,
        "provenance": provenance
    }

# Save final result
FINAL.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

print("Pipeline completed successfully!")
print(json.dumps(result, indent=2))
