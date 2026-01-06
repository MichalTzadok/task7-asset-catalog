import hashlib, shutil, json
from pathlib import Path
from datetime import datetime

def compute_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_unique_filename(filename: str, metadata: dict, upload_dir: Path, file_hash: str) -> str:
    base, ext = Path(filename).stem, Path(filename).suffix
    final = filename
    while (final in metadata and metadata[final] != file_hash) or (upload_dir / final).exists():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        final = f"{base}_{timestamp}{ext}"
    return final

def save_file(temp_path: Path, final_path: Path):
    shutil.move(temp_path, final_path)

def load_metadata(meta_file: Path) -> dict:
    return json.loads(meta_file.read_text()) if meta_file.exists() else {}

def update_metadata(meta_file: Path, metadata: dict, filename: str, file_hash: str):
    metadata[filename] = file_hash
    meta_file.write_text(json.dumps(metadata, indent=2))
