import json
import re
from pathlib import Path


PATTERNS = {
    "invoice_number": r"Invoice Number:\s*(.+)",
    "date": r"Date:\s*(.+)",
    "vendor": r"Vendor:\s*(.+)",
    "customer": r"Customer:\s*(.+)",
    "total_amount": r"Total Amount:\s*(.+)",
}


def extract_provenance(text):
    result = {}

    for field, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            result[field] = {
                "value": match.group(1).strip(),
                "provenance": {
                    "page": 1,
                    "source_text": match.group(0),
                },
            }

    return result


def main():
    markdown_file = Path("output/invoice.md")
    output_file = Path("output/provenance_output.json")

    text = markdown_file.read_text(encoding="utf-8")
    result = extract_provenance(text)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("Provenance extraction completed!")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
