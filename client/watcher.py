from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class Watcher:
    """Watch a folder for new or modified files and trigger a callback."""

    def __init__(self, folder: str, callback):
        self.folder = folder
        self.callback = callback

    class Handler(FileSystemEventHandler):
        def __init__(self, callback):
            self.callback = callback

        def on_created(self, event):
            if not event.is_directory:
                self.callback(event.src_path)

        def on_modified(self, event):
            if not event.is_directory:
                self.callback(event.src_path)

    def start(self):
        observer = Observer()
        observer.schedule(self.Handler(self.callback), self.folder, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
