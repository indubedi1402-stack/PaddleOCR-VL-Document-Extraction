from paddleocr_vl_document_extraction.provenance import extract_provenance
from paddleocr_vl_document_extraction.provenance_bbox import extract_bbox_provenance
from paddleocr_vl_document_extraction.run_pipeline import run_pipeline


def test_run_pipeline():
    data = {
        "res": {
            "rec_texts": [
                "Invoice Number: INV-001",
                "Date: 07 August 2026",
                "Vendor: ABC Technologies Pvt Ltd",
                "Customer: XYZ Company",
                "Total Amount: 52000",
            ],
            "dt_polys": [
                [[45, 144], [393, 144], [393, 229], [45, 229]],
                [[45, 144], [393, 144], [393, 229], [45, 229]],
                [[36, 305], [517, 305], [517, 390], [36, 390]],
                [[36, 305], [517, 305], [517, 390], [36, 390]],
                [[39, 678], [329, 678], [329, 706], [39, 706]],
            ],
        }
    }

    markdown = """Invoice Number: INV-001
Date: 07 August 2026
Vendor: ABC Technologies Pvt Ltd
Customer: XYZ Company
Total Amount: 52000"""

    schema = {
        "invoice_number": "string",
        "date": "string",
        "vendor": "string",
        "customer": "string",
        "total_amount": "number",
    }

    result = run_pipeline(data, markdown, schema)

    assert result["invoice_number"]["value"] == "INV-001"
    assert result["date"]["value"] == "07 August 2026"
    assert result["vendor"]["value"] == "ABC Technologies Pvt Ltd"
    assert result["customer"]["value"] == "XYZ Company"
    assert result["total_amount"]["value"] == 52000.0
    assert result["invoice_number"]["provenance"] is not None


def test_extract_provenance():
    text = """Invoice Number: INV-001
Date: 07 August 2026
Vendor: ABC Technologies Pvt Ltd
Customer: XYZ Company
Total Amount: 52000"""

    result = extract_provenance(text)

    assert result["invoice_number"]["value"] == "INV-001"
    assert result["invoice_number"]["provenance"]["page"] == 1
    assert "Invoice Number: INV-001" in result["invoice_number"]["provenance"]["source_text"]
    assert result["total_amount"]["value"] == "52000"


def test_extract_bbox_provenance():
    data = {
        "parsing_res_list": [
            {
                "block_content": "Invoice Number: INV-001",
                "block_bbox": [45, 144, 393, 229],
                "block_id": 1,
                "block_label": "text",
            },
            {
                "block_content": "Date: 07 August 2026",
                "block_bbox": [45, 144, 393, 229],
                "block_id": 1,
                "block_label": "text",
            },
            {
                "block_content": "Vendor: ABC Technologies Pvt Ltd",
                "block_bbox": [36, 305, 517, 390],
                "block_id": 2,
                "block_label": "text",
            },
            {
                "block_content": "Customer: XYZ Company",
                "block_bbox": [36, 305, 517, 390],
                "block_id": 2,
                "block_label": "text",
            },
            {
                "block_content": "Total Amount: 52000",
                "block_bbox": [39, 678, 329, 706],
                "block_id": 4,
                "block_label": "text",
            },
        ]
    }

    result = extract_bbox_provenance(data)

    assert result["invoice_number"]["value"] == "INV-001"
    assert result["date"]["value"] == "07 August 2026"
    assert result["vendor"]["value"] == "ABC Technologies Pvt Ltd"
    assert result["customer"]["value"] == "XYZ Company"
    assert result["total_amount"]["value"] == "52000"

    assert result["invoice_number"]["bbox"] == [45, 144, 393, 229]
    assert result["invoice_number"]["block_id"] == 1
    assert result["invoice_number"]["page"] == 1
