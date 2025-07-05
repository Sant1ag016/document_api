import os
import mysql.connector

def get_db_connection():
    """Obtiene la conexión a la base de datos usando variables de entorno."""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '00001'),
        database=os.getenv('MYSQL_DB', 'doc_info_db')
    )


def save_document_to_db(document_info):
    """Guarda la información del documento en la base de datos."""
    def none_if_empty(value):
        return value if value not in ("", None) else None

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insertar la información del documento en la base de datos
    cursor.execute("""
        INSERT INTO documents (doc_type, is_legible, raw_text, first_name, last_name, document_number, birth_date, birth_place, height, blood_type, gender, issue_date, issue_place, file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        document_info['doc_type'], 
        document_info['is_legible'], 
        document_info['raw_text'], 
        none_if_empty(document_info['first_name']), 
        none_if_empty(document_info['last_name']), 
        none_if_empty(document_info['document_number']), 
        none_if_empty(document_info['birth_date']), 
        none_if_empty(document_info['birth_place']), 
        none_if_empty(document_info['height']), 
        none_if_empty(document_info['blood_type']), 
        none_if_empty(document_info['gender']), 
        none_if_empty(document_info['issue_date']), 
        none_if_empty(document_info['issue_place']), 
        document_info['file_path']
    ))
    
    # Guardar los cambios en la base de datos
    conn.commit()
    
    # Cerrar la conexión
    cursor.close()
    conn.close()
    
    return "Document saved successfully"
