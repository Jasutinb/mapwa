import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IGNORED_DIRS = {
    os.path.normcase(os.path.abspath("tests"))
}


def is_ignored_path(path):
    normalized_path = os.path.normcase(os.path.abspath(path))
    return any(
        normalized_path == ignored_dir
        or normalized_path.startswith(ignored_dir + os.sep)
        for ignored_dir in IGNORED_DIRS
    )


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        print(f"\n[Watcher] Starting: {' '.join(self.command)}")
        # Use a new process group to ensure we can kill children if needed (on Windows it's different)
        self.process = subprocess.Popen(self.command)

    def on_modified(self, event):
        if event.is_directory:
            return
        if is_ignored_path(event.src_path):
            return
        if event.src_path.endswith('.py'):
            print(f"\n[Watcher] Detected change in {event.src_path}. Reloading...")
            self.start_process()

if __name__ == "__main__":
    path = "."
    command = [sys.executable, "main.py"]
    
    event_handler = ReloadHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print(f"[Watcher] Watching for changes in {os.path.abspath(path)}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()
