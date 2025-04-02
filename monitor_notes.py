import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

NOTES_DIR = "D:/GitHub/MyNotes"

def git_auto_upload():
    try:
        subprocess.run(["git", "add", "."], cwd=NOTES_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "自动提交"], cwd=NOTES_DIR, check=True)
        subprocess.run(["git", "push"], cwd=NOTES_DIR, check=True)
        print("Git 自动上传成功！")
    except subprocess.CalledProcessError as e:
        print(f"Git 上传失败: {e}")

class NotesHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"检测到文件变化: {event.src_path}")
        git_auto_upload()

if __name__ == "__main__":
    event_handler = NotesHandler()
    observer = Observer()
    observer.schedule(event_handler, path=NOTES_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()