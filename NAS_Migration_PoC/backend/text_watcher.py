from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging

logger = logging.getLogger(__name__)

class ContentFileHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback):
        self.file_path = str(file_path)
        self.callback = callback
        self.last_triggered = 0

    def on_modified(self, event):
        # Debounce to avoid double firing
        current_time = time.time()
        if event.src_path.endswith("migration_index.json") and (current_time - self.last_triggered > 1):
            logger.info("Content index modified. Triggering update...")
            self.last_triggered = current_time
            self.callback()

class IndexWatcher:
    def __init__(self, directory, filename, on_change_callback):
        self.observer = Observer()
        self.handler = ContentFileHandler(filename, on_change_callback)
        self.directory = directory
        
    def start(self):
        self.observer.schedule(self.handler, self.directory, recursive=False)
        self.observer.start()
        
    def stop(self):
        self.observer.stop()
        self.observer.join()
