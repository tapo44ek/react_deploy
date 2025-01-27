from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import os
import subprocess

app = FastAPI()

UPLOAD_DIR = "uploads"  # Директория для хранения загружаемых файлов
FILE_NAME = "react.zip"  # Фиксированное имя файла
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаём папку, если её нет


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload ZIP File</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f4f4f9;
            }
            h1 {
                color: #333;
            }
            form {
                margin-top: 20px;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            input[type="file"] {
                margin-bottom: 20px;
            }
            button {
                padding: 10px 15px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Upload ZIP File</h1>
        <p>Please select a ZIP file to upload. The file will be processed on the server.</p>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".zip" required/>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed.")

    # Путь к файлу с фиксированным именем
    file_path = os.path.join(UPLOAD_DIR, FILE_NAME)

    # Сохраняем файл, перезаписывая его
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Вызываем bash-скрипт с передачей пути к загруженному файлу
    try:
        result = subprocess.run(
            ["./process_zip.sh", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)

        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>File Processed</title>
            </head>
            <body>
                <h1>File Processed Successfully</h1>
                <p>Output from the script:</p>
                <pre>{result.stdout}</pre>
                <a href="/">Go Back</a>
            </body>
            </html>
            """,
            status_code=200,
        )
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error</title>
            </head>
            <body>
                <h1>Error Processing File</h1>
                <p>{str(e)}</p>
                <a href="/">Go Back</a>
            </body>
            </html>
            """,
            status_code=500,
        )