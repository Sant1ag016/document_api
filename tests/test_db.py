""" from app.models.db import save_document_to_db

def test_save_document():
    document_info = {
        "document_type": "Cédula de Ciudadanía",
        "document_number": "123456789",
        "first_name": "Juan",
        "last_name": "Pérez",
        "birth_date": "1990-01-01",
        "birth_place": "Bogotá"
    }
    result = save_document_to_db(document_info)
    assert result == "Document saved successfully"
"""  """ """