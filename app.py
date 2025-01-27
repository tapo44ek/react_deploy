from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import subprocess

app = FastAPI()

UPLOAD_DIR = "uploads"  # Директория для хранения загружаемых файлов
FILE_NAME = "react.zip"  # Фиксированное имя файла
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаём папку, если её нет


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

        return JSONResponse(
            content={
                "message": "File processed successfully!",
                "output": result.stdout,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running script: {e}")


@app.get("/")
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Upload ZIP File</h1>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".zip"/>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """