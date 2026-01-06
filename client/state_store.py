import json
from pathlib import Path
import portalocker

class StateStore:
    """Store file hashes locally to avoid duplicate uploads, supporting multiple clients."""
    
    def __init__(self, state_file=None):
        self.state_file = Path(state_file) if state_file else Path.home() / ".local/share/asset-client/state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_file.exists():
            with open(self.state_file, "w") as f:
                json.dump({"files": {}, "hashes": {}}, f, indent=2)

    def load(self):
        """Load the latest state from disk."""
        if self.state_file.exists():
            with portalocker.Lock(self.state_file, 'r', timeout=5) as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"files": {}, "hashes": {}}
        else:
            data = {"files": {}, "hashes": {}}
        return data

    def save(self, data):
        """Save state to disk safely using a lock."""
        with portalocker.Lock(self.state_file, 'w', timeout=5) as f:
            json.dump(data, f, indent=2)

    def exists(self, hash_val: str) -> bool:
        """Check if the file hash already exists (always loads latest state)."""
        data = self.load()
        return hash_val in data["hashes"]

    def add_file(self, file_path: str, hash_val: str):
        """Add a new file to state (reloads before adding to avoid race conditions)."""
        with portalocker.Lock(self.state_file, 'r+', timeout=5) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"files": {}, "hashes": {}}

            data["files"][file_path] = hash_val
            data["hashes"][hash_val] = file_path

            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
