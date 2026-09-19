import json
import re
from pathlib import Path

from paddleocr_vl_document_extraction.patterns import PATTERNS


def extract_fields(text, schema):
    result = {}

    for field, field_type in schema.items():
        pattern = PATTERNS.get(field)

        if not pattern:
            result[field] = None
            continue

        match = re.search(pattern, text, re.IGNORECASE)

        if not match:
            result[field] = None
            continue

        value = match.group(1).strip()

        if field_type == "number":
            value = float(value.replace(",", ""))

        result[field] = value

    return result


def main():
    markdown_file = Path("output/invoice.md")
    schema_file = Path("configs/extraction_schema.json")
    output_file = Path("output/structured_output.json")

    text = markdown_file.read_text(encoding="utf-8")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))

    result = extract_fields(text, schema)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("Schema extraction completed!")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
