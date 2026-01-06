# Asset Catalog

This project simulates storing **assets** (audio, images, videos, text, binary data, etc.) from multiple **remote clients** to a **centralized server**.

The client watches a folder and uploads new or modified files, while ensuring no duplicates are uploaded. The server stores the files and maintains metadata.

---

## Client

The client is a **CLI tool** that:

- Watches a folder for file changes.
- Uploads new or modified files to the server.
- Supports multiple clients running simultaneously.
- Does **not** modify or move the original files.
- Avoids duplicate uploads using a local **state file**.
- Stores the state file in OS-specific default locations (`~/.local/share` on Linux).

**Usage:**

```bash
python client/cli.py start <folder_to_watch> <server_url> <state_file>
```
Example:

```bash
python client/cli.py start watched http://127.0.0.1:8000 ~/.local/share/asset-client/state.json
```
## Server
The server is a simple HTTP server that:

- Accepts file uploads.

- Stores file contents and metadata in a local uploads/ folder.

- Prevents storing files with duplicate content.

Start the server:

```bash
uvicorn server.app:app --reload
```
# Testing
Automated tests are written in pytest and are organized in separate folders.

# Run client tests
pytest client/tests

# Run server tests
pytest server/tests

# Screenshots
Include screenshots as proof that my code works

