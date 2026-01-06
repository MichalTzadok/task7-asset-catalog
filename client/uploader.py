import requests
from pathlib import Path

class Uploader:
    """Upload files to the central server."""

    def __init__(self, server_url: str):
        self.server_url = server_url

    def upload(self, file_path: str) -> tuple[bool, str]:
        """Return (success, server_status)"""
        file_path_obj = Path(file_path)
        try:
            with open(file_path_obj, "rb") as f:
                files = {"file": (file_path_obj.name, f)}
                r = requests.post(f"{self.server_url}/upload", files=files)
            if r.status_code == 200:
                return True, r.json().get("status", "ok")
            else:
                return False, "error"
        except Exception as e:
            print(f"[ERROR] Upload failed: {file_path_obj.name}, reason: {e}")
            return False, "error"

