import os
import sys
import time
import atexit
import signal
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


LOCK_FILE = Path(__file__).with_suffix(".lock")


def is_process_running(pid):
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def terminate_process_tree(pid):
    if pid == os.getpid():
        return

    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return


def wait_for_process_exit(pid, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not is_process_running(pid):
            return True
        time.sleep(0.1)
    return not is_process_running(pid)


def acquire_single_instance_lock():
    try:
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            lock_pid = int(LOCK_FILE.read_text().strip())
        except (OSError, ValueError):
            lock_pid = 0

        if is_process_running(lock_pid):
            print(f"[Watcher] Replacing existing watcher with PID {lock_pid}.")
            terminate_process_tree(lock_pid)
            if not wait_for_process_exit(lock_pid):
                print(f"[Watcher] Could not stop existing watcher PID {lock_pid}.")
                sys.exit(1)

        LOCK_FILE.unlink(missing_ok=True)
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)

    with os.fdopen(fd, "w") as lock:
        lock.write(str(os.getpid()))

    atexit.register(release_single_instance_lock)


def release_single_instance_lock():
    try:
        lock_pid = int(LOCK_FILE.read_text().strip())
    except (OSError, ValueError):
        return

    if lock_pid == os.getpid():
        LOCK_FILE.unlink(missing_ok=True)


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
                self.process.wait(timeout=5)

        print(f"\n[Watcher] Starting: {' '.join(self.command)}")
        self.process = subprocess.Popen(self.command)

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            print(f"\n[Watcher] Detected change in {event.src_path}. Reloading...")
            self.start_process()

if __name__ == "__main__":
    acquire_single_instance_lock()

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
            try:
                event_handler.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                event_handler.process.kill()
                event_handler.process.wait(timeout=5)
    observer.join()
