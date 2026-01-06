import typer
import time
import requests
from pathlib import Path
from watcher import Watcher
from uploader import Uploader
from state_store import StateStore
from hasher import compute_hash
from config import WATCH_FOLDER, STATE_FILE, SERVER_URL

app = typer.Typer(help="Asset Catalog Client CLI")

def process_file(file_path: str, state: StateStore, uploader: Uploader):
    """Process a single file: compute hash, check local state, upload."""
    for attempt in range(5):
        try:
            hash_val = compute_hash(file_path)
            break
        except PermissionError:
            time.sleep(0.2)
    else:
        print(f"[ERROR] Cannot read file: {file_path}")
        return

    if state.exists(hash_val):
        print(f"[SKIP] {file_path} (already uploaded)")
        return

    success, server_status = uploader.upload(file_path)  # צריך להחזיר גם מצב מהסרבר
    if success:
        print(f"[{server_status.upper()}] {file_path}")
        if server_status == "ok":
            state.add_file(file_path, hash_val)
    else:
        print(f"[ERROR] Failed to upload: {file_path}")

@app.command()
def start(
    folder: str = typer.Argument(str(WATCH_FOLDER), help="Folder to watch"),
    server_url: str = typer.Argument(SERVER_URL, help="Server URL to upload files"),
    state_file: str = typer.Argument(str(STATE_FILE), help="File to store client state"),
):
    """Watch a folder and upload new/modified files to the server."""
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)

    print(f"Watching folder: {folder_path}")
    print(f"Uploading to server: {server_url}")
    print(f"State file: {state_file}")

    state = StateStore(state_file=state_file)
    uploader = Uploader(server_url)
    watcher = Watcher(str(folder_path), lambda f: process_file(f, state, uploader))

    try:
        watcher.start()
    except KeyboardInterrupt:
        print("\n[STOPPED] Watcher stopped by user.")

if __name__ == "__main__":
    app()

