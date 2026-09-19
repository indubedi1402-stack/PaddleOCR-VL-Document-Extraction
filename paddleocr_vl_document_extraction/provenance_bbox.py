import json
import re
from pathlib import Path

FIELDS = {
    "invoice_number": r"Invoice Number:\s*(.+)",
    "date": r"Date:\s*(.+)",
    "vendor": r"Vendor:\s*(.+)",
    "customer": r"Customer:\s*(.+)",
    "total_amount": r"Total Amount:\s*(.+)",
}


def extract_bbox_provenance(ocr_data):
    blocks = ocr_data.get("parsing_res_list", [])

    result = {}

    for field, pattern in FIELDS.items():
        result[field] = None

        for block in blocks:
            content = block.get("block_content", "")

            match = re.search(pattern, content, re.IGNORECASE)

            if match:
                result[field] = {
                    "value": match.group(1).strip(),
                    "source_text": match.group(0),
                    "page": 1,
                    "bbox": block.get("block_bbox"),
                    "block_id": block.get("block_id"),
                    "block_label": block.get("block_label"),
                }
                break

    return result


def main():
    ocr_file = Path("output/invoice_res.json")
    output_file = Path("output/final_provenance.json")

    data = json.loads(ocr_file.read_text(encoding="utf-8"))

    result = extract_bbox_provenance(data)

    output_file.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("Bounding-box provenance completed!")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
