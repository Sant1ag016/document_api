import os
import base64

def upload_to_local_storage(file_data, file_name, storage_path="uploaded_files/"):
    # Verificar si el directorio donde se guardarán los archivos existe, si no, crearlo
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    
    # Decodificar el archivo base64
    decoded_file = base64.b64decode(file_data)
    
    # Crear la ruta completa para el archivo
    file_path = os.path.join(storage_path, file_name)
    
    # Escribir el archivo en el sistema local
    with open(file_path, "wb") as f:
        f.write(decoded_file)
    
    return f"File saved locally at {file_path}"

def upload_to_gcp(file_data, file_name, bucket_name="your-bucket"):
    # Este código se mantendrá para cuando tengas GCP configurado.
    from google.cloud import storage
    
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    
    # Decodificar el archivo base64
    file_data = base64.b64decode(file_data)
    
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_data)
    return f"gs://{bucket_name}/{file_name}"
