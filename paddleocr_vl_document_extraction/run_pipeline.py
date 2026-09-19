import json
import re
from pathlib import Path

from paddleocr_vl_document_extraction.patterns import PATTERNS


def run_pipeline(data, markdown, schema):
    ocr = data.get("res", data)

    texts = ocr.get("rec_texts", [])
    boxes = ocr.get("dt_polys", [])

    result = {}

    for field, field_type in schema.items():
        pattern = PATTERNS.get(field)

        if not pattern:
            result[field] = None
            continue

        match = re.search(pattern, markdown, re.IGNORECASE)

        if not match:
            result[field] = None
            continue

        value = re.sub(r"\*\*", "", match.group(1)).strip()

        if field_type == "number":
            value = float(re.sub(r"[^0-9.\-]", "", value))

        provenance = None

        for i, text in enumerate(texts):
            if re.search(pattern, text, re.IGNORECASE):
                provenance = {
                    "page": 1,
                    "source_text": text,
                    "bbox": boxes[i],
                    "text_index": i,
                }
                break

        result[field] = {
            "value": value,
            "provenance": provenance,
        }

    return result


def main():
    ocr_json = Path("output/invoice_res.json")
    markdown_file = Path("output/invoice.md")
    schema_file = Path("configs/extraction_schema.json")
    final_file = Path("output/final_result.json")

    data = json.loads(ocr_json.read_text(encoding="utf-8"))
    markdown = markdown_file.read_text(encoding="utf-8")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))

    result = run_pipeline(data, markdown, schema)

    final_file.parent.mkdir(parents=True, exist_ok=True)
    final_file.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("Pipeline completed successfully!")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
