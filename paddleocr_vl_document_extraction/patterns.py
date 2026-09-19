PATTERNS = {
    "invoice_number": r"Invoice Number:\s*(.+?)(?=Date:|$)",
    "date": r"Date:\s*(.+?)(?=Vendor:|$)",
    "vendor": r"Vendor:\s*(.+?)(?=Customer:|$)",
    "customer": r"Customer:\s*(.+?)(?=\s*Total Amount:|$)",
    "total_amount": r"Total Amount:\s*(.+)",
}
