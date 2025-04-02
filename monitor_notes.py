import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 确保 Git 在 PATH 中
os.environ["PATH"] += r";C:\Program Files\Git\bin"

NOTES_DIR = r"D:\GitHub\MyNotes"
GIT_EXE = r"C:\Program Files\Git\bin\git.exe"

class NotesHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"检测到文件变化: {event.src_path}")
        self.safe_git_sync()

    def safe_git_sync(self):
        try:
            subprocess.run([GIT_EXE, "pull"], cwd=NOTES_DIR, check=True)
            subprocess.run([GIT_EXE, "add", "."], cwd=NOTES_DIR, check=True)
            subprocess.run([GIT_EXE, "commit", "-m", "自动提交"], cwd=NOTES_DIR, check=True)
            subprocess.run([GIT_EXE, "push"], cwd=NOTES_DIR, check=True)
            print("同步成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: {e.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    handler = NotesHandler()
    observer = Observer()
    observer.schedule(handler, NOTES_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()