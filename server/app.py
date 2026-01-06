from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from server.utils import (
    compute_hash,
    get_unique_filename,
    save_file,
    load_metadata,
    update_metadata,
)

app = FastAPI(title="Asset Catalog Server")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
META_FILE = UPLOAD_DIR / "metadata.json"
metadata = load_metadata(META_FILE)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    temp_path = UPLOAD_DIR / f"tmp_{file.filename}"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    file_hash = compute_hash(temp_path)

    # If file with same content exists
    if file_hash in metadata.values():
        temp_path.unlink()
        existing_file = [fname for fname, h in metadata.items() if h == file_hash][0]
        return JSONResponse(status_code=200, content={
            "message": "File with same content already exists",
            "filename": existing_file
        })

    final_filename = get_unique_filename(file.filename, metadata, UPLOAD_DIR, file_hash)
    save_file(temp_path, UPLOAD_DIR / final_filename)
    update_metadata(META_FILE, metadata, final_filename, file_hash)

    return {"filename": final_filename, "hash": file_hash, "message": "File uploaded successfully"}
