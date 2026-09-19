import json
import re
from pathlib import Path


def run_pipeline(data, markdown, schema):
    blocks = data.get("parsing_res_list", [])

    # Support test data and actual PaddleOCR output
    ocr = data.get("res", data)

    if "rec_texts" in ocr:
        texts = ocr.get("rec_texts", [])
        boxes = ocr.get("dt_polys", [])
    else:
        texts = [
            block.get("block_content", "")
            for block in blocks
        ]
        boxes = [
            block.get("block_bbox")
            for block in blocks
        ]

    # Robust patterns for merged OCR text
    patterns = {
        "invoice_number": r"Invoice Number:\s*(.*?)(?=\s*Date:|$)",
        "date": r"Date:\s*(.*?)(?=\s*Vendor:|$)",
        "vendor": r"Vendor:\s*(.*?)(?=\s*Customer:|$)",
        "customer": r"Customer:\s*(.*?)(?=\s*Total Amount:|$)",
        "total_amount": r"Total Amount:\s*([0-9.,\-]+)",
    }

    result = {}

    for field, field_type in schema.items():

        pattern = patterns.get(field)

        if pattern is None:
            result[field] = None
            continue

        # Search full OCR/markdown text
        match = re.search(
            pattern,
            markdown,
            re.IGNORECASE | re.DOTALL
        )

        if match is None:
            result[field] = None
            continue

        value = match.group(1).strip()

        # Convert number fields
        if field_type == "number":
            number = re.sub(
                r"[^0-9.\-]",
                "",
                value
            )

            try:
                value = float(number)
            except ValueError:
                value = None

        # Find provenance
        provenance = None

        for i, text in enumerate(texts):

            text_match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.DOTALL
            )

            if text_match:

                provenance = {
                    "page": 1,
                    "source_text": text_match.group(0).strip(),
                    "bbox": (
                        boxes[i]
                        if i < len(boxes)
                        else None
                    ),
                    "text_index": i,
                }

                break

        result[field] = {
            "value": value,
            "provenance": provenance,
        }

    return result


def main():

    ocr_json = Path(
        "output/invoice_res.json"
    )

    markdown_file = Path(
        "output/invoice.md"
    )

    schema_file = Path(
        "configs/extraction_schema.json"
    )

    final_file = Path(
        "output/final_result.json"
    )

    # Load OCR result
    data = json.loads(
        ocr_json.read_text(
            encoding="utf-8"
        )
    )

    # Use invoice.md if available.
    # Otherwise build text from PaddleOCR blocks.
    if markdown_file.exists():

        markdown = markdown_file.read_text(
            encoding="utf-8"
        )

    else:

        blocks = data.get(
            "parsing_res_list",
            []
        )

        markdown = "\n".join(
            block.get(
                "block_content",
                ""
            )
            for block in blocks
        )

    # Load schema
    schema = json.loads(
        schema_file.read_text(
            encoding="utf-8"
        )
    )

    # Run pipeline
    result = run_pipeline(
        data,
        markdown,
        schema
    )

    # Save result
    final_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final_file.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        "Pipeline completed successfully!"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
