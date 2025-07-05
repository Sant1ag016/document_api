""" from app.services.ocr_service import process_document

def test_process_document():
    # Test with mock base64 data
    mock_base64_data = "<mock_base64_string>"
    document_type, document_text = process_document(mock_base64_data)
    assert document_type == "Cédula de Ciudadanía"
    assert "document number" in document_text
 """