<<<<<<< HEAD
# document_api
=======
# Document API

This project is a FastAPI application designed for document processing, including functionalities such as Optical Character Recognition (OCR) and file uploads to cloud storage. 

## Project Structure

```
document_api/
├── app/
│   ├── __init__.py                 # Initializes the FastAPI application
│   ├── config.py                    # Configuration for the app (DB, GCP, etc.)
│   ├── controllers/                 # Controllers for handling API routes
│   │   └── document_controller.py    # Document processing logic (routes)
│   ├── services/                    # Business logic and processing services
│   │   ├── ocr_service.py            # OCR service for extracting text from images/PDFs
│   │   └── cloud_storage.py          # GCP storage service for uploading files (optional)
│   ├── models/                      # Models for database interactions
│   │   └── db.py                     # MySQL database connection and queries
│   ├── utils/                       # Utility functions (base64, validation, etc.)
│   │   └── base64_util.py           # Functions for handling base64 encoding/decoding
│   ├── logs/                        # Log files for the application
│   └── main.py                      # Entry point for running the FastAPI app
├── tests/                           # Tests folder (unit and integration tests)
│   ├── __init__.py
│   ├── test_document_processing.py   # Tests for document validation and OCR
│   └── test_api.py                  # Tests for API routes (POST /upload, etc.)
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Files or folders to exclude from version control
├── Dockerfile                       # Dockerfile for the application container
├── docker-compose.yml               # Docker Compose file to orchestrate services
└── README.md                        # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd document_api
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

4. **Access the API:**
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the API documentation and interact with the endpoints.

## Usage

- **Upload Document:** Use the `/upload` endpoint to upload documents for processing.
- **OCR Processing:** The application will extract text from the uploaded documents using the OCR service.

## Testing

To run the tests, use the following command:
```
pytest tests/
```



# Document API

API para extracción automática de información relevante de documentos colombianos (cédulas, pasaportes, etc.) usando OCR y procesamiento de texto.

---

## Requisitos

- **Python 3.9+**
- **Tesseract OCR** instalado en el sistema  
  - [Descargar para Windows](https://github.com/tesseract-ocr/tesseract/wiki#windows)
- **MySQL** (para almacenamiento de resultados)

---

## Instalación

1. **Clona el repositorio y entra a la carpeta del proyecto:**
    ```sh
    git clone <url-del-repo>
    cd document_api
    ```

2. **Crea y activa un entorno virtual:**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # En Windows
    # source venv/bin/activate  # En Linux/Mac
    ```

3. **Instala las dependencias:**
    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Instala el modelo de spaCy para español:**
    ```sh
    python -m spacy download es_core_news_sm
    ```

5. **Configura Tesseract en tu sistema:**
    - Instala Tesseract y agrega su ruta (`C:\Program Files\Tesseract-OCR`) a la variable de entorno `PATH`.
    - Verifica en terminal:
      ```sh
      tesseract --version
      ```

6. **Configura la base de datos MySQL:**
    - Crea la base de datos y la tabla `documents` según tu modelo.
    - Ajusta las variables en el archivo `.env`:
      ```
      MYSQL_HOST=localhost
      MYSQL_USER=root
      MYSQL_PASSWORD=tu_contraseña
      MYSQL_DB=doc_info_db
      ```

---

## Ejecución local

```sh
uvicorn app.main:app --reload
```

La API estará disponible en [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Uso de la API

### **Subir un documento**

- **Endpoint:** `POST /upload`
- **Tipo de body:** `form-data`
- **Campo:**  
  - `file`: Selecciona el archivo (imagen o PDF)

**Ejemplo en Postman:**
- Selecciona `POST`
- URL: `http://localhost:8000/upload`
- En "Body" selecciona `form-data`, agrega un campo `file` y adjunta tu archivo.

---

## Estructura del proyecto

```
app/
  controllers/
    document_controller.py
  services/
    ocr_service.py
    cloud_storage.py
  models/
    db.py
  utils/
    base64_util.py
  exceptions/
    exceptions.py
  main.py
  config.py
```

---

## Notas técnicas

- El OCR usa Tesseract y preprocesamiento de imágenes para mejorar la calidad.
- El texto extraído se procesa con expresiones regulares y spaCy para identificar campos clave.
- Los resultados se almacenan en una base de datos MySQL.
- Soporta documentos en español e inglés.

---

## Despliegue con Docker (opcional)

Si prefieres usar Docker:

1. **Construye la imagen:**
    ```sh
    docker build -t document-api .
    ```

2. **Ejecuta el contenedor:**
    ```sh
    docker run -p 8000:8000 --env-file .env document-api
    ```

---

## Problemas comunes

- **Tesseract no encontrado:**  
  Asegúrate de instalar Tesseract y agregarlo al `PATH` del sistema.
- **Error de modelo spaCy:**  
  Ejecuta `python -m spacy download es_core_news_sm`.
- **Error de conexión MySQL:**  
  Verifica usuario, contraseña y existencia de la base de datos.

---


## License

This project is licensed under the MIT License. See the LICENSE file for more details.
>>>>>>> 123c24ab (first commit)
