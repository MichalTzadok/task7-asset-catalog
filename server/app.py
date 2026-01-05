from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json, hashlib, shutil
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Asset Catalog Server")

# --- CORS ---
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "*",  # Allows all origins, convenient for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

META_FILE = UPLOAD_DIR / "metadata.json"
if META_FILE.exists():
    with open(META_FILE, "r") as f:
        metadata = json.load(f)
else:
    metadata = {}

def compute_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_unique_filename(filename: str) -> str:
    """If filename exists, append timestamp to make it unique"""
    base = Path(filename).stem
    ext = Path(filename).suffix
    while (UPLOAD_DIR / filename).exists():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"{base}_{timestamp}{ext}"
    return filename

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Create temporary file
    temp_path = UPLOAD_DIR / f"tmp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    file_hash = compute_hash(temp_path)

    # Check if same name & same content exists
    if file.filename in metadata and metadata[file.filename] == file_hash:
        os.remove(temp_path)
        return JSONResponse(status_code=200, content={
            "message": "File already exists with same content",
            "filename": file.filename
        })

    # If same name exists but different content, generate unique name
    final_filename = file.filename
    if file.filename in metadata and metadata[file.filename] != file_hash:
        final_filename = get_unique_filename(file.filename)

    file_path = UPLOAD_DIR / final_filename
    shutil.move(temp_path, file_path)

    # Update metadata
    metadata[final_filename] = file_hash
    with open(META_FILE, "w") as f:
        json.dump(metadata, f)

    return {"filename": final_filename, "hash": file_hash, "message": "File uploaded successfully"}
